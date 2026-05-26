import math
import random
from core_model import Blockchain, Transaction


def poisson_sample(mean_value, rng):
    if mean_value <= 0:
        return 0
    l_value = math.exp(-mean_value)
    k = 0
    p = 1.0
    while p > l_value:
        k += 1
        p *= rng.random()
    return k - 1


def run_simulation(config):
    rng = random.Random(config.get("seed", 42))
    blockchain = Blockchain()

    current_time = 0
    tx_counter = 1
    next_block_time = max(1, poisson_sample(config["avg_block_time"], rng))

    stats = []
    all_confirmed_transactions = []

    while current_time < config["duration"]:
        blockchain.release_visible_transactions(current_time)
        blockchain.release_visible_blocks(current_time)

        tx_count = poisson_sample(config["tx_rate_mean"], rng)
        for _ in range(tx_count):
            tx = Transaction(tx_id=tx_counter, created_at=current_time)
            tx.visible_at = current_time + rng.randint(
                config["network_delay_min"],
                config["network_delay_max"]
            )
            blockchain.add_pending_transaction(tx)
            tx_counter += 1

        confirmed_count = 0
        avg_confirmation_time = None
        mined_this_step = False

        if current_time >= next_block_time:
            propagation_delay = rng.randint(
                config["network_delay_min"],
                config["network_delay_max"]
            )
            block = blockchain.create_block(
                current_time=current_time,
                block_size=config["block_size"],
                propagation_delay=propagation_delay
            )
            confirmed_count = len(block.transactions)
            mined_this_step = True

            if confirmed_count > 0:
                confirmation_times = [
                    tx.confirmation_time
                    for tx in block.transactions
                    if tx.confirmation_time is not None
                ]
                avg_confirmation_time = sum(confirmation_times) / len(confirmation_times)
                all_confirmed_transactions.extend(block.transactions)

            next_interval = max(1, poisson_sample(config["avg_block_time"], rng))
            next_block_time = current_time + next_interval

        resource_cost = (
            tx_count * 0.25
            + len(blockchain.mempool) * 0.06
            + len(blockchain.pending_transactions) * 0.03
            + confirmed_count * 0.28
            + (0.5 if mined_this_step else 0.0)
        )

        stats.append({
            "time": current_time,
            "generated_in_step": tx_count,
            "visible_mempool_size": len(blockchain.mempool),
            "pending_transaction_count": len(blockchain.pending_transactions),
            "confirmed_in_step": confirmed_count,
            "avg_confirmation_time_step": avg_confirmation_time,
            "resource_cost": round(resource_cost, 3),
            "chain_length": len(blockchain.chain),
            "next_block_time": next_block_time,
        })

        current_time += 1

    blockchain.release_visible_transactions(current_time)
    blockchain.release_visible_blocks(current_time)

    total_confirmed = len(all_confirmed_transactions)
    throughput = total_confirmed / config["duration"] if config["duration"] > 0 else 0

    if total_confirmed > 0:
        overall_avg_confirmation = sum(
            tx.confirmation_time
            for tx in all_confirmed_transactions
            if tx.confirmation_time is not None
        ) / total_confirmed
    else:
        overall_avg_confirmation = None

    summary = {
        "duration": config["duration"],
        "tx_rate_mean": config["tx_rate_mean"],
        "block_size": config["block_size"],
        "avg_block_time": config["avg_block_time"],
        "final_visible_mempool_size": len(blockchain.mempool),
        "pending_transaction_count": len(blockchain.pending_transactions),
        "blocks_visible_in_chain": len(blockchain.chain),
        "total_confirmed_transactions": total_confirmed,
        "throughput_tps": round(throughput, 3),
        "avg_confirmation_time": round(overall_avg_confirmation, 3) if overall_avg_confirmation is not None else None,
    }

    return stats, summary
class Transaction:
    def __init__(self, tx_id, created_at):
        self.tx_id = tx_id
        self.created_at = created_at
        self.visible_at = created_at
        self.confirmed_at = None

    @property
    def confirmation_time(self):
        if self.confirmed_at is None:
            return None
        return self.confirmed_at - self.created_at


class Block:
    def __init__(self, block_id, transactions, mined_at, visible_at):
        self.block_id = block_id
        self.transactions = transactions
        self.mined_at = mined_at
        self.visible_at = visible_at


class Blockchain:
    def __init__(self):
        self.chain = []
        self.mempool = []
        self.pending_transactions = []
        self.pending_blocks = []
        self.next_block_id = 1

    def add_pending_transaction(self, tx):
        self.pending_transactions.append(tx)

    def release_visible_transactions(self, current_time):
        newly_visible = [tx for tx in self.pending_transactions if tx.visible_at <= current_time]
        self.pending_transactions = [tx for tx in self.pending_transactions if tx.visible_at > current_time]
        self.mempool.extend(newly_visible)

    def add_pending_block(self, block):
        self.pending_blocks.append(block)

    def release_visible_blocks(self, current_time):
        visible_blocks = [b for b in self.pending_blocks if b.visible_at <= current_time]
        self.pending_blocks = [b for b in self.pending_blocks if b.visible_at > current_time]

        for block in visible_blocks:
            self.chain.append(block)
            confirmed_ids = {tx.tx_id for tx in block.transactions}
            self.mempool = [tx for tx in self.mempool if tx.tx_id not in confirmed_ids]

    def create_block(self, current_time, block_size, propagation_delay):
        selected = self.mempool[:block_size]

        for tx in selected:
            tx.confirmed_at = current_time

        block = Block(
            block_id=self.next_block_id,
            transactions=selected,
            mined_at=current_time,
            visible_at=current_time + propagation_delay
        )
        self.next_block_id += 1
        self.add_pending_block(block)
        return block
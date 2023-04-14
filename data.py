from collections import defaultdict

from pysyncobj import SyncObj, SyncObjConf, replicated_sync


class Data(SyncObj):
    def __init__(self, self_node, other_nodes):
        self_node_norm = self_node.replace(':', '_')
        cfg = SyncObjConf(dynamicMembershipChange=True, journalFile=f'.journals/journal_{self_node_norm}.journal')
        super().__init__(self_node, other_nodes, cfg)
        self._balances = defaultdict(int)

    @replicated_sync
    def withdraw(self, account, amount):
        if self._balances[account] >= amount:
            self._balances[account] -= amount
            return True
        return False

    @replicated_sync
    def deposit(self, account, amount):
        self._balances[account] += amount

    @replicated_sync
    def transfer(self, from_account, to_account, amount):
        if self._balances[from_account] >= amount:
            self._balances[from_account] -= amount
            self._balances[to_account] += amount
            return True
        return False

    def get_balance(self, account):
        return self._balances[account]

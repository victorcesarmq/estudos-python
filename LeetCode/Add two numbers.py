# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        ListNode_constructor = ListNode

        dummy_head = ListNode_constructor(0)
        atual = dummy_head
        vai_um = 0

        while l1 and l2:
            soma_total = l1.val + l2.val + vai_um
            vai_um = soma_total // 10
            atual.next = ListNode_constructor(soma_total % 10)
            atual = atual.next
            l1 = l1.next
            l2 = l2.next

        l_restante = l1 if l1 else l2

        while l_restante:
            if vai_um == 0:
                atual.next = l_restante
                return dummy_head.next

            soma_total = l_restante.val + vai_um
            vai_um = soma_total // 10
            atual.next = ListNode_constructor(soma_total % 10)
            atual = atual.next
            l_restante = l_restante.next

        if vai_um:
            atual.next = ListNode_constructor(vai_um)

        return dummy_head.next
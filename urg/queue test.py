class Queue():
    cQ_size = 4
    cQ = [0] * cQ_size
    front = rear = 0

    def isEmpty(self):
        return self.front == self.rear

    def isFull(self):
        return (self.rear + 1) % len(self.cQ) == self.front

    def enQueue(self, item):
        if self.isFull():
            print("Queue is Full")
        else:
            self.rear = (self.rear + 1) % len(self.cQ)
            self.cQ[self.rear] = item

    def deQueue(self):
        if self.isEmpty():
            print("Queue is Empty")
        else:
            self.front = (self.front + 1) % len(self.cQ)
            return self.cQ[self.front]

    def lenOfQueue(self):
        return len(self.cQ)

    def printAll(self):
        tmp = []
        for i in self.cQ:
            tmp.append(i)
        return tmp

if __name__ == "__main__":
    q = Queue()

    q.enQueue('A')  # front 0 rear 2 [0, 'A', 'B', 0]
    print(q.printAll())
    q.enQueue('B')  # front 0 rear 2 [0, 'A', 'B', 0]
    print(q.printAll())
    print(q.deQueue())  # 'A' # front 1 rear 2 [0, 'A', 'B', 0]
    print(q.printAll())
    q.enQueue('C')  # front 1 rear 3 [0, 'A', 'B', 'C']
    print(q.printAll())
    q.enQueue('D')  # front 1 rear 0 ['D', 'A', 'B', 'C']
    print(q.printAll())
    q.enQueue('E')  # Queue is Full -> (rear+1) % 4 == front
    print(q.printAll())
    print(q.deQueue())  # 'B' # front 2 rear 0 ['D', 'A', 'B', 'C']
    print(q.printAll())
    q.enQueue('E')  # front 2 rear 1 ['D', 'E', 'B', 'C']
    print(q.printAll())




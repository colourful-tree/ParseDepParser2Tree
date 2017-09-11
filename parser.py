# coding: utf-8

class Node(object):
    def __init__(self):
        self.value = ""
        self.childrens = None
        self.father = None

class Tree(object):
    def __init__(self):
        self.count = 0
        self.origin_sents = []
        self.sents = []
        self.trees = []
        self.trunks = []
        self.cluster = {}

    def load_data(self):
        with open("origin.txt", "r") as fin:
            for i in fin:
                self.origin_sents.append(i.strip())

        with open("test.txt", "r") as fin:
            sent = ""
            for i in fin:
                if i.strip() == "":
                    self.sents.append(sent)
                    sent = ""
                else:
                    sent += i
        for i in range(len(self.sents)):
            self.sents[i] = self.sents[i].replace(" ", "")
            self.sents[i] = self.sents[i].replace("\n", "")
        if len(self.sents) == len(self.origin_sents):
            print "count right"
        else:
            print len(self.sents), len(self.origin_sents)
        self.count = len(self.sents)
        #for i in self.sents:
        #    print i

    def print_tree(self):
        def print_each(s):
            if len(s)  == 0:
                return
            stack = []
            for i in s:
                print i.value
                if i.childrens != None:
                    for child in i.childrens:
                        stack.append(child)
            print "--"
            print_each(stack)

        for i in self.trees:
            s = [i]
            print_each(s)
            print "-------"

    def cluster_similarity_tree(self, max_dep = 5):
        def get_sent_trunk():
            def bfs(s, dep, max_dep, res):
                if dep == max_dep or len(s) == 0:
                    return
                stack = []
                for i in s:
                    res.append(i.value)
                    if i.childrens != None:
                        for child in i.childrens:
                            stack.append(child)
                bfs(stack, dep + 1, max_dep, res)
            for i in self.trees:
                trunk = []
                bfs([i], 0, max_dep, trunk)
                self.trunks.append(" ".join(trunk))

        get_sent_trunk()
        for i in range(len(self.trunks)):
            if self.trunks[i] in self.cluster:
                self.cluster[self.trunks[i]].append(i)
            else:
                self.cluster[self.trunks[i]] = [i]

        print len(self.cluster)
        for k, v in self.cluster.items():
            if len(v) > 1:
                for i in v:
                    print self.origin_sents[i]
                print "-------"

    def print_res(self):
        print "done"

    def parse(self):
        for sent in self.sents:
            p = sent.find("(")
            stack = ["("]
            root = Node()
            self.trees.append(root)
            pos = root
            while len(stack) > 0 and p >= 0:
                n_left = sent.find("(", p+1)
                n_right = sent.find(")", p+1)
                n = -1
                if n_left == -1:
                    n = n_right
                    stack.pop()
                elif n_right == -1:
                    n = n_left
                    break
                else:
                    if n_left > n_right:
                        n = n_right
                        stack.pop()
                    else:
                        n = n_left
                        stack.append("(")
                #print n_left, n_right
                #   (ROOT(IP(NP(NR夏朝))(VP(VV建立))(PU。)))
                if p+1 != n:
                    value = sent[p+1:n]
                    #print p, n, value
                    tmp = Node()
                    tmp.father = pos
                    tmp.value = value
                    if pos.childrens is None:
                        pos.childrens = [tmp]
                    else:
                        pos.childrens.append(tmp)
                    pos = pos.childrens[-1]
                else:
                    pos = pos.father
                p = n


tree = Tree()
tree.load_data()
tree.parse()
tree.cluster_similarity_tree()
#tree.print_tree()

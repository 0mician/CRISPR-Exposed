class Fastas:
    """ Construct an object from a fasta file (containing one or more sequences) 
    Each fasta sequence in a file has a header, and a sequence. They are maintained 
    in a list, where each element is an object Fasta.
    """

    class Fasta:
        def __init__(self, header, seq):
            self.header = header
            self.seq = seq
        
        def __str__(self):
            return "Header: %s\nSequence: %s\n" % (self.header, self.seq)

    def __init__(self, file):
        self.fastas = []
        self.__set_content_from_file(file)
        self.__validate_fasta()

    def __iter__(self):
        i = 0
        size = len(self.fastas)
        while(i < size):
            yield self.fastas[i]
            i += 1

    def __getitem__(self, pos):
        return self.fastas[pos]

    def is_empty(self):
        return len(self.fastas) == 0

    def __validate_fasta(self):
        if(not self.fastas):
            raise ValueError

    def __read_file(self, file):
        fasta_file = open(file, 'r')
        content = fasta_file.readlines()
        return content

    def __set_content_from_file(self, file):
        content = self.__read_file(file)
        size = len(content)
        i = 0
        while(i < size):
            sequence = header = ""
            if(content[i].startswith(">")):
                header = content[i][1:].strip("\n") # header, stripped of >
                i += 1
                while(i < size and not content[i].startswith(">")):
                    sequence += content[i].strip("\n")
                    i += 1
            self.fastas.append(Fastas.Fasta(header, sequence))
    

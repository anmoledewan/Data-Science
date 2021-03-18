from collections import defaultdict as defaultlist
from collections import OrderedDict as Orderedlist
import copy as copy

class interPretr(object):
    vertices = list()
    edges = list()
    READ_MODE = 'r'
    APPEND_MODE = 'a'
    WORD_SPLITTER = '/'
    OUTPUT_FILE = './outputPS25.txt'
    PROMPT_SPLITTER = ':'

    def __init__(self):
        self.interp_lang_graph = defaultlist(list)
        self.edges_connection = list()
        self.languages= set()
        self.candidates= set()

    def runPromptFile(self, promptFile):
        promptFile = open(promptFile, self.READ_MODE)
        lines = promptFile.readlines()
        intrepetr.showAll()

        for line in lines:
            word = line.strip()
            inputLine = word.split(self.PROMPT_SPLITTER)
            
            if(inputLine[0].strip()=='showMinList'):
                intrepetr.displayHireList()

                
            if(inputLine[0].strip()=='searchLanguage'):
                intrepetr.displayCandidates(inputLine[1].strip())

            if(inputLine[0].strip()=='DirectTranslate'):
                intrepetr.findDirectTranslator(inputLine[1].strip(),inputLine[2].strip())

            if(inputLine[0].strip()=='TransRelation'):
                intrepetr.findTransRelation(inputLine[1].strip(),inputLine[2].strip())
            
    
        
        
    def readApplications(self, inputfile):
        inputFile = open(inputfile, self.READ_MODE)
        lines = inputFile.readlines()

        def addVertices(inputLine):
            inputLine = inputLine.strip()
            inputLine = inputLine.split(self.WORD_SPLITTER)

            for element in inputLine:
                element = element.strip()
                if element not in self.vertices:
                    self.vertices.append(element)

        def addEdges(inputLine):
            inputLine = inputLine.strip()
            inputLine = inputLine.split(self.WORD_SPLITTER)
            edge_parent = inputLine[0].strip()

            for element in inputLine:
                element = element.strip()
                if element != edge_parent:
                    self.edges.append((edge_parent, element))

        for line in lines:
            line = line.strip()
            addVertices(line)
            addEdges(line)


        def plotGraph(edges):

            def align_edge(plotgraph, edgeSrc, edgeDest):
                plotgraph[edgeSrc].append(edgeDest)

            for edge in edges:
                align_edge(self.interp_lang_graph, edge[0], edge[1])


        def get_edges(graph):
            edges = set()
            for node in graph:
                for neighbour in graph[node]:
                    edges.add((node, neighbour))
                    edges.add((neighbour,node))

            return list(edges)

        plotGraph(self.edges)
        self.edges_connection = get_edges(self.interp_lang_graph)
        
        for element in self.edges:
            self.candidates.add(element[0])
            self.languages.add(element[1])

        self.interp_lang_graph1 = defaultlist(list)
        for ele in self.edges_connection:
            self.interp_lang_graph1[ele[0]].append(ele[1])

        self.interp_lang_graph1 = Orderedlist(sorted(self.interp_lang_graph1.items(), key=lambda item: len(item[1]), reverse=True))
        

    def showAll(self):

        outputFile = open(self.OUTPUT_FILE, self.APPEND_MODE)
        outputFile.write('\n--------Function showAll--------')

        outputFile.write('\nTotal no. of candidates: {:}'.format(len(self.candidates)))
        outputFile.write('\nTotal no. of languages: {:}'.format(len(self.languages)))

        outputFile.write('\n\nList of candidates: ')
        candidates = list(self.candidates)
        for cand in candidates:
            outputFile.write("\n{:}".format(str(cand).strip()))

        outputFile.write('\n\nList of languages: ')
        languages = list(self.languages)
        for lang in languages:
            outputFile.write("\n{:}".format(str(lang).strip()))
        
        outputFile.write("\n\n-----------------------------------------\n")
        outputFile.close()

    def displayCandidates(self, language):

        outputFile = open(self.OUTPUT_FILE, self.APPEND_MODE)
        outputFile.write('\n\n--------Function displayCandidates --------')
        outputFile.write('\nList of Candidates who can speak {:}:'.format(language))

        for ele in self.edges_connection:
            if ele[1] == language:
                outputFile.write("\n{:}".format(ele[0]))
                
        outputFile.write("\n-----------------------------------------\n")
        outputFile.close()

    def findDirectTranslator(self, langA, langB):

        outputFile = open(self.OUTPUT_FILE, self.APPEND_MODE)
        outputFile.write('\n\n--------Function findDirectTranslator --------')
        outputFile.write('\nLanguage A: {:}'.format(langA))
        outputFile.write('\nLanguage B: {:}'.format(langB))
        candidate_list = list()

        for cand,langs in self.interp_lang_graph.items():
            if langA in langs and langB in langs:
                candidate_list.append(cand)
                
        if(len(candidate_list)==0):
            outputFile.write("\nDirect Translator: No.")
        else:
            outputFile.write("\nDirect Translator: Yes, ")
            outputFile.write(', '.join(candidate_list))
            outputFile.write(" can translate.")
            
        outputFile.write("\n-----------------------------------------\n")
        outputFile.close()



    def displayHireList(self):
        outputFile = open(self.OUTPUT_FILE, self.APPEND_MODE)
        outputFile.write('\n\n--------Function displayHireList--------')


        languagz = copy.deepcopy(self.languages)
        sorted_graph = Orderedlist(sorted(self.interp_lang_graph.items(), key=lambda item: len(item[1]), reverse=True))
        candidate_list = list()

        for cand,langs in sorted_graph.items():
            candidate_list.append(cand)
            for lang in langs:
                if lang in languagz:
                    languagz.remove(lang)

            if len(languagz)==0:
                break

        outputFile.write('\nNo of candidates required to cover all languages: {:}'.format(len(candidate_list)))
        for cand in candidate_list:
            outputFile.write('\n{:}'.format(cand))
            for lang in sorted_graph[cand]:
                outputFile.write(' / {:}'.format(lang))
        
        outputFile.write("\n-----------------------------------------\n")
        outputFile.close()

    

    def findTransRelation(self, langA, langB):
        trans_path = list()
        outputFile = open(self.OUTPUT_FILE, self.APPEND_MODE)
        outputFile.write('\n\n--------Function findTransRelation --------')
        outputFile.write('\nLanguage A: {:}'.format(langA))
        outputFile.write('\nLanguage B: {:}'.format(langB))


        def find_path(graph, inputLang, outputLang, candSeq=[]):

            if inputLang not in self.vertices or outputLang not in self.vertices:
                return list()

            if inputLang == outputLang:
                return candSeq + [outputLang]

            candSeq = candSeq + [inputLang]
            for node in graph[inputLang]:
                if node not in candSeq:
                    candSeqpath = find_path(graph, node, outputLang, candSeq)
                    if candSeqpath:
                        return candSeqpath

        trans_path = find_path(self.interp_lang_graph1,langA,langB)

        if len(trans_path) > 0:
            outputFile.write("\nRelated: Yes, ")
            outputFile.write(' > '.join(trans_path))
        else:
            outputFile.write("\nRelated: No")

        outputFile.write("\n\n-----------------------------------------\n")
        outputFile.close()




if __name__ == '__main__':
    intrepetr = interPretr()
    intrepetr.readApplications('./inputPS25.txt')
    intrepetr.runPromptFile('./promptsPS25.txt')

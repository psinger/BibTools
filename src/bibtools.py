from __future__ import division

__author__ = 'psinger'

import collections
import sys
import os
import shutil
from titlecase import titlecase

def parseAux(f):
    check = set()
    for line in open(f):
        columns = line.strip().split("{")
        print columns
        if "bibcite" in columns[0] or "citation" in columns[0]:
            check.add(columns[1][:-1])

    return check

def getElements(f, detailed=False):
    """
    Gets elements of a bib file
    :param f: file pointer
    :param detailed: boolean, if True a fine-grained dict is returned
    :return: dict of elements
    """
    dict = {}

    if detailed:
        ele = {}
    else:
        ele = ""
    check = False
    for line in f:
        line = line.strip()

        if not line:
            continue

        if line[0] == '@':
            columns = line.split('{')

            #dic['type'] = typ.strip(',')
            key = columns[1].strip(',')

            if detailed:
                type = columns[0].strip().lower()
                ele["type"] = type

            check = True

        if check:

            if line[0] == '}':

                if detailed:
                    dict[key] = ele
                    ele = {}
                else:
                    dict[key] = ele
                    ele = ""

                check = False

            else:
                if detailed:
                    #print line
                    if line[0] != '@':
                        columns = line.split("=")
                        #print line
                        if len(columns) == 2:
                            val = columns[1]
                            key_ele = columns[0].strip().lower()
                            val = val.strip('" ,{}')
                            ele[key_ele] = val
                        elif len(columns) > 2:
                            val = "".join(columns[1:])
                            key_ele = columns[0].strip().lower()
                            val = val.strip(' "{},')
                            ele[key_ele] = val
                        else:
                            ele[key_ele] += " " + line.strip(' "{},')

                            #print line
                            #print ele[key_ele]

                else:
                    ele += line
                    ele += "\n"

    print dict
    return dict


def replaceElements(f1, f2, out):
    """
    Replaces elements of first bib file with those of second
    :param f1: file1 path
    :param f2: file2 path
    :param out: out file path
    :return: None
    """

    f1 = open(f1)
    f2 = open(f2)
    out = open(out, "w")

    ele_first = getElements(f1)
    ele_second = getElements(f2)

    for k,v in ele_first.iteritems():

        if k in ele_second:
            if "labstats" in ele_second[k]:
                print ele_second[k]
            out.write(ele_second[k])
        else:
            out.write(v)
        out.write("}\n\n")


    return


def mergeElements(f1, f2, out):
    """
    Merges two bib files and replaces elements of f1 with those of f2
    :param f1: file1 path
    :param f2: file2 path
    :param out: out file path
    :return: None
    """

    f1 = open(f1)
    f2 = open(f2)
    out = open(out, "w")

    ele_first = getElements(f1)
    ele_second = getElements(f2)

    z = dict(ele_first.items() + ele_second.items())

    for k,v in ele_second.iteritems():
        out.write(v)
        out.write("\n")

    return

SUFFIXES = {1: 'st', 2: 'nd', 3: 'rd'}
def ordinal(num):
    # I'm checking for 10-20 because those are the digits that
    # don't follow the normal counting scheme.
    if 10 <= num % 100 <= 20:
        suffix = 'th'
    else:
        # the second parameter is a default.
        suffix = SUFFIXES.get(num % 10, 'th')
    return str(num) + suffix

def processConference(s, replacer):



    s = titlecase(s)



    s = s.replace("Proceedings of the", "")
    s = s.replace("Proceedings of", "")



    for i in reversed(range(100)):
        s = s.replace(ordinal(i), "")

    s = ''.join([i for i in s if not i.isdigit()])

    s = s.strip()

    if "SYRCODIS" in s:
        print s

    for k,v in replacer.iteritems():
        if s == k:
            s = s.replace(k,v)

    return s

def processJournal(s):

    s = titlecase(s)

    return s.strip()


def cleanElements(f, out):

    input = open(f)
    out = open(out, "w")

    ele = getElements(input, detailed=True)

    # for k,v in ele.iteritems():
    #     if v["type"] == "@article":
    #         if "volume" not in v:
    #             print v
    #             #sys.exit()

    replacer_conf = collections.OrderedDict({
        "AAAI Conference on Artificial Intelligence": "Conference on Artificial Intelligence",
        "Conference on Information and Knowledge Management": "International Conference on Information and Knowledge Management",
        "Cambridge Philosophical Society": "Mathematical Proceedings of the Cambridge Philosophical Society",
        "In Workshop on Wordnet and Other Lexical Resources, Second Meeting of the North AmeQFrican Chapter of the Association for Computational Linguistics": "Workshop on WordNet and Other Lexical Resources",
        "Workshop on Ontology Learning and Population (OLP)": "Workshop on Ontology Learning and Population",
        "Sixth International Conference on Knowledge Capture": "International Conference on Knowledge Capture",
        "Computers and Communications, . Proceedings., Second IEEE Symposium On": "Symposium on Computers and Communications",
        "ACM International Conference on Information and Knowledge Management":"International Conference on Information and Knowledge Management",
        "ACM SIGKDD International Conference on Knowledge Discovery and Data Mining": "International Conference on Knowledge Discovery and Data Mining",
        "Twentieth International Joint Conference for Artificial Intelligence": "International Joint Conference for Artificial Intelligence",
        "Twenty-Fifth AAAI Conference on Artificial Intelligence": "Conference on Artificial Intelligence",
        "AAAI Conference on Artificial Intelligence": "Conference on Artificial Intelligence",
        "European Conference on the Semantic Web: Research and Applications": "European Semantic Web Conference",
        "Proc. Of the Int'l. Conf. On Research in Computational Linguistics": "International Conference on Research in Computational Linguistics",
        "International World Wide Web Conference": "International Conference on World Wide Web",
        "Conference on Computational Linguistics - Volume": "Conference on Computational Linguistics",
        "ACM Conference on Hypertext and Hypermedia":"Conference on Hypertext and Hypermedia",
        "Annual International ACM SIGIR Conference on Research and Development in Information Retrieval" : "International Conference on Research and Development in Information Retrieval",
        "Proceedings of Sem-Search 2008 CEUR Workshop": "Workshop on Semantic Search",
        "In:  EACL": "Workshop on Making Sense of Sense: Bringing Computational Linguistics and Psycholinguistics Together",
        "Demonstration Papers at HLT-NAACL": "Human Language Technologies: The  Annual Conference of the North American Chapter of the Association for Computational Linguistics",
        "International Joint Conference on Artifical Intelligence": "International Joint Conference on Artificial Intelligence",
        "AAAI Spring Symposium : Wisdom of the Crowd" : "Spring Symposium on Wisdowm of the Crowd",
        "National Conference on Artificial Intelligence - Volume": "Conference on Artificial Intelligence",
        "WWW' Workshop on 'Making Sense of Microposts'": "Workshop on Making Sense of Microposts",
        "National Conference on Artificial Intelligence": "Conference on Artificial Intelligence",
        "SIGCHI Conference on Human Factors in Computing Systems":"Conference on Human Factors in Computing Systems",
        "SYRCODIS  Colloquium on Databases and Information Systems Saint-Petersburg, Russia, May -,":"Colloquium on Databases and Information Systems",
        "The Semantic Web: Semantics and Big Data":"European Semantic Web Conference",
        "International Conference on Conference on Information \& Knowledge Management" : "International Conference on Information and Knowledge Management",
        "In  Conference on Artificial Intelligence" : "Conference on Artificial Intelligence",
        "Twenty-Eighth Australasian Conference on Computer Science - Volume" : "Australasian Conference on Computer Science",
        "Data Mining (ICDM),  IEEE  International Conference On": "International Conference on Data Mining",
        "Ninth ACM SIGKDD International Conference on Knowledge Discovery and Data Mining": "International Conference on Knowledge Discovery and Data Mining",
        "European Conference on Machine Learning and Knowledge Discovery in Databases (ECML/PKDD)": "European Conference on Machine Learning and Knowledge Discovery in Databases",
        "Fifth ACM SIGKDD International Conference on Knowledge Discovery and Data Mining":"International Conference on Knowledge Discovery and Data Mining",
        "ACM SIGCOMM Conference on Internet Measurement Conference": "Internet Measurement Conference",
        "ACM Conference on Hypertext and Social Media":"Conference on Hypertext and Social Media",
        "Eighth International AAAI Conference on Weblogs and Social Media": "International Conference on Web and Social Media",
        "ACM SIGCOMM Conference on Internet Measurement Conference": "Internet Measurement Conference",
        "ACM Conference on Electronic Commerce": "Conference on Electronic Commerce",
        "Privacy, Security, Risk and Trust (PASSAT),  International Conference on and  International Confernece on Social Computing (SocialCom)": "International Conference on Social Computing",
        "Icwsm": "International Conference on Web and Social Media",
        "Companion Publication of the  International Conference on World Wide Web Companion":"International Conference on World Wide Web Companion",

        }
    )

    replacer_article = collections.OrderedDict({
        "J. Artif. Int. Res.": "Journal of Artificial Intelligence Research",
        "IEEE Trans. Pattern Anal. Mach. Intell." : "IEEE Transactions on Pattern Analysis and Machine Intelligence",
        "Artif. Intell.": "Artificial Intelligence",
        "Psychon. Bull. Rev." : "Psychonomic Bulletin \& Review",
        "Comput. Linguist.": "Computational Linguistics",
        "BMC Med Res Methodol": "BMC Medical Research Methodology",
        "IEEE Trans. On Knowl. And Data Eng." : "IEEE Transactions on Knowledge and Data Engineering",
        "Commun. ACM" : "Communications of the ACM",
        "ACM Transactions on Computer-Human Interaction (TOCHI)": "ACM Transactions on Computer-Human Interaction",
        "ACM SIGCOMM Computer Communication Review": "Computer Communication Review",
        "Ieee Transactions on Pattern Analysis and Machine Intelligence" : "IEEE Transactions on Pattern Analysis and Machine Intelligence",
        "Inf. Retr.":"Information Retrieval",
        "Journal of the Royal Statistical Society. Series B (Methodological)" : "Journal of the Royal Statistical Society: Series B",
        "ACM Trans. Intell. Syst. Technol." : "ACM Transactions on Intelligent Systems and Technology",
        "Mem Cognit": "Memory \& Cognition",
        "Software Engineering, IEEE Transactions On": "IEEE Transactions on Software Engineering",
        "Web Semantics: Science, Services and Agents on the World Wide Web":"Journal of Web Semantics",
        "SIGKDD Explor. Newsl." : "ACM SIGKDD Explorations Newsletter",
        "PLoSOne":"PLOS ONE",
        "Journal of Experimental Psychology. Applied": "Journal of Experimental Psychology: Applied"
        }
    )

    conf_needed = ["title", "author", "year", "booktitle"]
    conf_considered = ["title", "author", "year", "booktitle", "url", "note"]
    journal_needed = ["title", "author", "pages", "year", "journal", "volume"]
    journal_considered = ["title", "author", "publisher", "pages", "year", "journal", "number", "volume", "issue", "doi", "url", "note"]
    book_needed = ["title", "author", "year", "publisher"]
    book_considered = ["title", "author", "year", "publisher"]

    ele = collections.OrderedDict(sorted(ele.items()))

    for k,v in ele.iteritems():
        out.write(v["type"] + "{" + k + ",\n")

        if v["type"] == "@article":
            for n in journal_needed:
                if n not in v.keys():
                    print k, v["type"], "missing", n

        if v["type"] == "@inproceedings":
            for n in conf_needed:
                if n not in v.keys():
                    print k, v["type"], "missing", n

        if v["type"] == "@book":
            for n in book_needed:
                if n not in v.keys():
                    print k, v["type"], "missing", n

        for x,y in v.iteritems():
            if x == "type":
                continue

            if v["type"] == "@inproceedings":
                if x not in conf_considered:
                    continue
                if x == "booktitle":
                    y = processConference(y, replacer_conf)

            if v["type"] == "@article":
                if x not in journal_considered:
                    continue
                if x == "journal":

                    if "arxiv" in y or "CoRR" in y:
                        print k, "arxiv journal may need fix"

                    y = processJournal(y)

            if v["type"] == "@book":
                if x not in book_considered:
                    continue

            if x == "note":
                print k, "check note"

            #y = y.replace('{', "").replace("}", "")
            out.write(x + " = {" + y + "},\n")
        out.write("}\n\n")


    return

def limitAux(f, aux, out):

    check = parseAux(aux)

    f = open(f)
    out = open(out, "w")

    ele = getElements(f, detailed=True)

    ele = collections.OrderedDict(sorted(ele.items()))

    for k,v in ele.iteritems():

        if k not in check:
            continue
        out.write(v["type"] + "{" + k + ",\n")
        for x,y in v.iteritems():
            if x == "type":
                continue
            out.write(x + " = {" + y + "},\n")
        out.write("}\n\n")


def backupFile(f):

    shutil.copyfile(f, f+".backup")


def main():


    #always call backup first
    backupFile("bib.bib")

    #removes all references in the bib file that are not in the aux file (i.e., not references in tex)
    limitAux("bib.bib.backup", "bib.aux", "bib.bib")

    #again backup
    backupFile("bib.bib")

    #this function cleans the elements
    cleanElements("bib.bib.backup", "bib.bib")



if __name__ == "__main__":
    main()

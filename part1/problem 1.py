#python 2.7.6
import os

## a global variable used to store the sum of path, size and counts for each directory
storeArray = []

## contract: root_path --> array
## purpose: recursively go through all directories in the root path, count the total number of 
##          public, private, try and catch in java files, get the size of files, add them up for 
##          each directory, then store the name, size, number of public, private, try, catch of
##          each directory into an array
def searchPath(root):
    countPub = 0
    countPri = 0
    countTry = 0
    countCat = 0
    files = os.listdir(root)
    size = 0
    for f in files:
        f = root + '/' + f
        if not os.path.isdir(f):
            extension = os.path.splitext(f)[1]
            if extension == '.java':
                countPub += countUse(f, 'public')
                countPri += countUse(f, 'private')
                countTry += countUse(f, 'try')
                countCat += countUse(f, 'catch')
                size += os.path.getsize(f)
        else:
            subPub, subPri, subTry, subCat, subSize= searchPath(f)
            countPub += subPub
            countPri += subPri
            countTry += subTry
            countCat += subCat
            size += subSize
    storeArray.append((root, size, countPub, countPri, countTry, countCat))
    return countPub, countPri, countTry, countCat, size


## contract: file_name, keyword --> number_of_keyword_in_file
## purpose: to count the number of keyword that appeared in the file, excluding comments
def countUse(fileName, keyword):
    count = 0
    isComment = False
    fo = open(fileName, "r")
    for line in fo:
        # trim single comment line
        commentSingle = line.find('//')
        line = line[:commentSingle]
        wordArray = line.split()
        for w in wordArray:
            # check if the word is comment or not
            commentMultipleBegin = w.find('/*')
            if commentMultipleBegin != -1:
                w= w[:commentMultipleBegin]
                isComment = True
            commentMultipleEnd = w.find('*/')
            if commentMultipleEnd != -1:
                w= w[commentMultipleEnd:]
                isComment = False
            # count when keyword is found and is not comment
            if isComment == False and w.find(keyword) != -1:
                count += 1     
    fo.close()
    return count



##contract: root_path --> None
##purpose: initionalize the searching process, print out the information, and empty the stored information
def getStats(root):
    print 'Input: getStats("' + root + '")'
    searchPath(root)
    while storeArray:
        root, size, countPub, countPri, countTry, countCat = storeArray.pop()
        print root + ':'
        print str(size) + ' bytes   ' + str(countPub) + ' public   '+ str(countPri) + ' private   ' + str(countTry) + ' try   ' + str(countCat) + ' catch   '
        

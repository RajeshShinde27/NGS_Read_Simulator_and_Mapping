#!/usr/bin/python3
__author__ = "Rajesh Shinde"
__credits__ = ["Rajesh Shinde", "Aditya Pathak"]
__version__ = "1.0"
__email__ = "rajesh27071992@gmail.com"
__status__ = "Development"

#### Imports #######
import random

#### File Read - Writes ######

try:
    fh = open("hs_ref_GRCh38.p2_chr1.fa", "r")
except FileNotFoundError:
    print("Sequence file is not present in the working directory!")

try:
    fh2 = open("qual_values_2","r")
except FileNotFoundError:
    print("Dummy quality value file is not present in the working directory!")

try:
    fout = open("RandomSeq.fastq","w")
except FileExistsError:
    print("Simulated Fastq file is already present!")


##### Global Variables ########

seq_string = ''
qual_string = ''
No_of_seq = 100000
No_of_iterations = No_of_seq/2
read_length = 50

######## File data handlers #########
for line in fh:
    if (line.startswith(">")):
        continue
    else:
        seq_string = seq_string + line.strip()
        
for l in fh2:
    qual_string = qual_string + l.strip()

######### Functions #########


''' This function introduces 1 base error
    in the read provided as input '''

def IntroduceError(seq1):
    list1 = ["A","G","T","C","N"]
    random_pos = random.randint(0,len(seq1)-1)
    new_nucleotide = random.choice(list1)
    
    if (new_nucleotide != seq1[random_pos]):
        seq1 = seq1[:random_pos] + new_nucleotide + seq1[random_pos + 1:]
    return seq1
    
''' This function select 2 random reads of 50bp from Genome and
    input one of the two read to the IntroduceError function.
    This is because the required error rate is 0.01 and hence,
    only one of 2 reads can have base with error '''

def random_seq(sequence):
    pos1 = random.randint(0,(len(sequence)-read_length))
    return_seq1 = sequence[pos1:pos1+read_length]
    pos2 = random.randint(0,(len(sequence)-read_length))
    return_seq2 = sequence[pos2:pos2+read_length]

    read_with_error = random.randint(1,2)
    if (read_with_error == 1):
        return_seq1 = IntroduceError(return_seq1)
    else:
        return_seq2 = IntroduceError(return_seq2)
    return (return_seq1,return_seq2)

''' This function return 50 randomly selected quality values
    qualities string '''
def random_qual(num, qualities):
    return_qual= ''
    for x in range(num):    
        return_qual = return_qual + random.choice(qualities)
    return return_qual


j = 1 ## Variable to append read_number at the end of each read

''' This function writes 2 reads at a time to the output fastq file.
    One of these reads has a base with error '''

def NGSFastqSimulator(sequence1, qualities):
    global j
    for i in range(int(No_of_iterations)):
        (read_sequence1 , read_sequence2) = random_seq(sequence1)

        ### Writing 1st Read ###
        fout.write("@RandomSequence_"+str(j)+"\n")
        fout.write(read_sequence1 + "\n")
        fout.write("+"+"\n")
        fout.write(random_qual(read_length,qual_string)+"\n")

        ### Writing 2nd Read ######
        fout.write("@RandomSequence_"+str(j+1)+"\n")
        fout.write(read_sequence2 + "\n")
        fout.write("+"+"\n")
        fout.write(random_qual(read_length,qual_string)+"\n")
        j = j+2

############ Function call ##########
NGSFastqSimulator(seq_string, qual_string)

#### Message to print on successful generation of file #######
print("File generation completed")    

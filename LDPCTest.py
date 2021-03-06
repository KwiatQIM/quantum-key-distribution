'''
Created on Jul 1, 2016

@author: laurynas
'''
from SlepianWolf import encode,SW_LDPC
from SW_prep import transitionMatrix_data,transitionMatrix_data2,transitionMatrix_data2_python,sequenceProbMatrix,randomMatrix,set_printoptions,nan,append
from numpy import loadtxt,array
from ParityCheckMatrixGen import gallager_matrix


if __name__ == '__main__':
    alice = loadtxt("./DarpaQKD/LDPC_alice_ttags8_1000.txt")
    bob = loadtxt("./DarpaQKD/LDPC_bob_ttags8_1000.txt")
#  ========== encode ===================
    column_weight = 3
    row_weight = 4
    
    frame_size = 8
    
    total_string_length = len(alice)
#     print alice
#     number_of_parity_check_eqns_gallager = int(total_string_length*column_weight/row_weight)
#     parity_matrix = gallager_matrix(number_of_parity_check_eqns_gallager, total_string_length, column_weight, row_weight)
#     parity_matrix = array([[ 1,  1,  1,  1,  0,  0,  0,  0,  0,  0,  0,  0,],
#                      [ 0,  0,  0,  0,  1,  1,  1,  1,  0,  0,  0,  0,],
#                      [ 0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,],
#                      [ 0,  0,  1,  0,  1,  0,  1,  0,  0,  0,  1,  0,],
#                      [ 1,  1,  0,  0,  0,  0,  0,  1,  0,  0,  0,  1,],
#                      [ 0,  0,  0,  1,  0,  1,  0,  0,  1,  1,  0,  0]])
#     print "Parity matrix\n",parity_matrix
#     print "column weight of first column",sum(parity_matrix[:,0])
    number_of_parity_check_eqns_gallager = int(total_string_length*0.52)
    k = 0
    for i in range(10):
        parity_matrix = randomMatrix(total_string_length, number_of_parity_check_eqns_gallager,3)
        a=array([])
        for i in range(parity_matrix.shape[0]):
    #         print sum(parity_matrix[i,:])
            a = append(a,sum(parity_matrix[i,:]))
        print min(a),"-",max(a)
#         print parity_matrix
        syndromes=encode(parity_matrix,alice,alphabet=frame_size)
#         print "syndromes: ", syndromes
    #  ======================================
        
    # ============ decode ===================
        decoder='bp-fft'
        iterations=70
        frozenFor=5
        
        set_printoptions(threshold=nan)
        transition_matrix = transitionMatrix_data2_python(bob,alice,frame_size)
        prior_probability_matrix = sequenceProbMatrix(bob,transition_matrix)
    #   
    #     print "prior_probability_matrix\n",prior_probability_matrix
    #     print "Transition matrix\n",transition_matrix
        belief_propagation_system = SW_LDPC(parity_matrix, syndromes, prior_probability_matrix, original=alice,decoder=decoder)
        guess = belief_propagation_system.decode(iterations=iterations,frozenFor=frozenFor)
        print "was ERROR",sum(alice!=bob)/float(len(alice))
        print "KEY CORRECTNESS",sum(guess == alice)/float(len(alice))
        if sum(guess == alice)/float(len(alice)) == 1.0:
            print "@@$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$-"
            break
            k+=1
    print k
    print min(a),"-",max(a)
        
        
      
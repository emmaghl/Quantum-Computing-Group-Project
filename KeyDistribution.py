from QuantumComputerSimulator import QuantumComputer, Test

import matplotlib.pyplot as plt
import sys
import numpy as np
import time
import random

# Step 0 - Set up n qubit register

# Step 1 - Generate a random bit string n long, this is the message, A_bits

# Step 2 - generate a random bit string n long, this is the corresponding, A_bases

# Step 3 - Set up each qubit corresponding to the combination of A_bases and A_bits

# Step ! - Interception

# Step 4 - B_measure, set up B_bases to measure_measure each qubit against that bases

# Step 5 - Compare the random choice of bases to achieve secret key of bits for both A and B! 

# Step 6 - Create random sample of key to check.

# Step 7 - Check sample keys for interception, 

# Step 8 - Disgard sample keys to get secret key for both A and B

def measure_any(qnum, state, register ):
    register_conjugate = np.conjugate(register)
    register_ket = register_conjugate.T
    inner_register = qc.Matrix.matrix_multiply(register, register_ket)
    inner_register = inner_register.matrix

    if state == 0:
        matrix = qc.gate_logic([(["M0"], [[qnum]])])
        matrix = matrix.matrix
    elif state == 1:
        matrix = qc.gate_logic([(["M1"], [[qnum]])])
        matrix = matrix.matrix

    inner_register_M = qc.Matrix.matrix_multiply(matrix, inner_register)
    inner_register_M = inner_register_M.matrix
    QProb = np.trace(inner_register_M)

    if (np.random.rand() < QProb):
        result = 0
    else:
        result = 1
    return result

def main():
    print("You are acting as a communication channel for person A to send secret messages to person B.")
    n = int(input('How long would person A like their bit message to be?: '))

    global qc

    qc = QuantumComputer(n, 'Dense')



    # Step 0 ---------------------------------------------------------------------------------------------------------------------------------------------------------------

    register = np.array([[1, 0]])

    w = 2**(n) - 2

    for i in range(w):
        register = np.append(register, [0])

    register = np.array([register]).T

    #print("You are acting as a communication channel for person A to send a secret message to person B")

    #print('Step 0 complete: Qubit register setup')
    # Step 1 ---------------------------------------------------------------------------------------------------------------------------------------------------------------

    A_bits = np.random.randint(2, size=n)


    print('Step 1 complete:', 'A bits =', A_bits, '!This is not shared publicly!')
    #Step 2 ---------------------------------------------------------------------------------------------------------------------------------------------------------------

    A_bases = np.random.randint(2, size=n)

    print('Step 2 complete:', 'A bases =', A_bases, '!This is not shared publicly!')
    #Step 3 ---------------------------------------------------------------------------------------------------------------------------------------------------------------

    for i in range(n):
        j = A_bases[i]
        k = A_bits[i]
        if j == 0:
            if k == 0:
                pass
            else:
                circuit = qc.gate_logic( [(["X"], [[i]])] )
                circuit = circuit.matrix
                register = qc.Matrix.matrix_multiply(circuit, register)
                register = register.matrix
        if j == 1:
            if k == 0:
                circuit = qc.gate_logic( [(["H"], [[i]])] )
                circuit = circuit.matrix
                register = qc.Matrix.matrix_multiply(circuit, register)
                register = register.matrix
            else:
                circuit_1 = qc.gate_logic( [(["X"], [[i]])] )
                circuit_1 = circuit_1.matrix
                circuit_2 = qc.gate_logic( [(["H"], [[i]])] )
                circuit_2 = circuit_2.matrix
                circuit = circuit_2.dot(circuit_1)
                register = qc.Matrix.matrix_multiply(circuit, register)
                register = register.matrix

    #print('Step 3 complete: Qubits encoded')
    print('Person A has their secretly encoded message ready to send to person B.')

    # Step Interception ---------------------------------------------------------------------------------------------------------------------------------------------------------------

    y = int(input('Do you want to intercept and try and read their message? Yes = 1, No = 0 :'))

    if y == 1:
        C_bases = np.random.randint(2, size=n)
        measurement_intercept = []
        register_intercept = []
        for i in range(n):
            g = C_bases[i]
            if g == 0:
                result = measure_any(i, 0, register)
                register_intercept.append(result)
                measurement_intercept.append(result)

            else:
                circuit = qc.gate_logic([(["H"], [[i]])])
                circuit = circuit.matrix
                register = qc.Matrix.matrix_multiply(circuit, register)
                register = register.matrix
                result = measure_any(i, 0, register)
                register_intercept.append(result)
                measurement_intercept.append(result)
                measurement_intercept.append(result)
        register = [[]]
        zero = np.array([(1, 0)])
        zero = zero.T
        one = np.array([(0, 1)])
        one = one.T
        for i in range(n):
            q = register_intercept[i]
            if i == 0:
                if q == 0:
                    register = np.append(register, zero)
                else:
                    register = np.append(register, one)
                register = np.matrix(register)
                register = register.T
            else:
                if q == 0:
                    register = qc.Matrix.tensor_prod(register, zero)
                    register = register.matrix
                else:
                    register = qc.Matrix.tensor_prod(register, one)
                    register = register.matrix
        print('Interception completed, this is the message you read:', measurement_intercept)
    else:
        pass

    # Step 4 ---------------------------------------------------------------------------------------------------------------------------------------------------------------

    B_bases =  np.random.randint(2, size=n)

    measurement = []
    for i in range(n):
        g = B_bases[i]
        if g == 0:
            result = measure_any(i, 0, register)
            measurement.append(result)

        else:
            circuit = qc.gate_logic( [(["H"], [[i]])] )
            circuit = circuit.matrix
            register = qc.Matrix.matrix_multiply( circuit, register)
            register = register.matrix
            result = measure_any(i, 0, register)
            measurement.append(result)

    print('Person B has measured the message.')
    print('Person A shares the bases which they measured the message with, and vice versa so that they can both create a key.')
    #print('Step 4 complete:')
    #print('B Bases =', B_bases, '!This is not shared publicly!')
    #rint('Measured B bits =', measurement, '!This is not shared publicly!')
    # Step 5 ---------------------------------------------------------------------------------------------------------------------------------------------------------------

    B_Key = []

    for i in range(n):
        a = A_bases[i]
        b = B_bases[i]
        c = measurement[i]
        if a == b:
            B_Key.append(c)
        else:
            pass

    A_Key = []
    for i in range(n):
        a = A_bases[i]
        b = B_bases[i]
        c = A_bits[i]
        if a == b:
            A_Key.append(c)
        else:
            pass

    #print('Step 5 complete')
    #print('A Key =', A_Key , 'This is not shared publicly')
    #print('B Key =', B_Key, 'This is not shared publicly')

    # Step 6 ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    print('Now a random sample is generated to test if the keys for person A and B are secure.')
    sample_A = []
    sample_B = []

    j = len(A_Key)
    l = len(B_Key)

    if j == l:
        #print('Lengths match')
        #print('Length of Key =', j)
        pass
    else:
        print('Error in Key length')
        exit()


    number_of_samples = round(j*0.5)

    s = random.sample(range(0, j), number_of_samples)

    print (s)

    for i in s:
        f = A_Key[i]
        h = B_Key[i]
        sample_A.append(f)
        sample_B.append(h)

    print('Person A and person B share their random sample of the message they measured using the bases already shared:')
    print('A random sample = ', sample_A)
    print('B random sample = ', sample_B)

    # Step 7 ---------------------------------------------------------------------------------------------------------------------------------------------------------------

    j = len(sample_A)
    l = len(sample_B)

    if j == l:
            pass
    else:
            print('Error in sample length')


    for i in range(j):
        p = 1
        if sample_A[i] == sample_B[i]:
            p = p + 1
        else:
            print('You were caught listening!')
            exit()
    print('Secret Key is probably secure.')



    #print('Step 7 complete:', p)
    # Step 8 ---------------------------------------------------------------------------------------------------------------------------------------------------------------

    j = len(A_Key)
    t = range(0, j)
    t = list(t)

    for i in s:
        t.remove(i)

    A_secret_key = []
    B_secret_key = []

    for i in t:
        A_secret_key.append(A_Key[i])
        B_secret_key.append(B_Key[i])

    print('Both person A and person B have their secret keys now:')
    print('A Secret Key =', A_secret_key, 'These are not shared publicaly, but are used to encript messages.')
    print('B Secret Key =', B_secret_key, 'These are not shared publicaly, but are used to encript messages.')


if __name__=="__main__":
    main()

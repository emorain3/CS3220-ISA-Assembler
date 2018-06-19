import sys
import re


""" Local Vars """
finalInstrList = []
secondInstrList = []
initialInstrList = []
thirdInstrList = []
fourthInstrList = []
variables = {}
labelBase = 0
inputFileName = sys.argv[1]
outputFileName = sys.argv[2]
if outputFileName.endswith(".mif") is False:
	outputFileName = sys.argv[2] + ".mif"
	print "Output File Name", outputFileName

print "Files Received ", inputFileName, outputFileName
print("\n")

outputFile = open(outputFileName, "w")

with open(inputFileName) as inputFile:
	initialInstrList = inputFile.readlines()

print("\n")

print "Initial Instruction List \n", initialInstrList



""" Remove All Comments """
for i in range(len(initialInstrList)):
	print "instruction: ", initialInstrList[i]
	commentIndex = initialInstrList[i].find(";")
	if(commentIndex != -1):
		initialInstrList[i] = initialInstrList[i][0:commentIndex]
	# initialInstrList[i] = initialInstrList[i].split(';')
	print "instruction NOW: ", initialInstrList[i], "\n"

print "Comments removed\n ", initialInstrList, "\n"



print "----"
""" Create Dictionary of Variable (.NAME and .ORIG) Assignments """
for i in range(len(initialInstrList)):
	if "ORIG" in initialInstrList[i]:
		print "variable assignment instruction: ", initialInstrList[i]
		if ".ORIG" not in initialInstrList[i]:
			print "Error on Line ", i+1, "ORIG should be .ORIG"
			sys.exit()
		else:
			if labelBase == 0:
				origArray = initialInstrList[i].split()
				print "Temp origArray: ", origArray, "\n"
				labelBase = origArray[1].strip()
				labelBase = int(labelBase, 16) / 4
				variables["labelBase"] = labelBase
		secondInstrList.append(initialInstrList[i])

	elif "NAME" in initialInstrList[i]:
		print "variable assignment instruction: ", initialInstrList[i]
		if ".NAME" not in initialInstrList[i]:
			print "Error on Line ", i+1, "NAME should be .NAME"
			sys.exit( )
		else:
			nameArray = initialInstrList[i].split("=")
			print "Temp nameArray: ", nameArray, "\n"
			variableValue = nameArray[1].replace("\n", "")
			nameArray = nameArray[0].split()
			print "Temp nameArray: ", nameArray, "\n"
			varableName = nameArray[-1]
			variables[varableName] = str(variableValue)
			
	elif ":" in initialInstrList[i]:
		print "variable assignment instruction: ", initialInstrList[i]
		labelArray = initialInstrList[i].split(":")
		print "Temp labelArray: ", labelArray, "\n"
		labelName = labelArray[0]
		variables[labelName] = 0
		
	else:
		secondInstrList.append(initialInstrList[i])




		# REMOVE labelBase key FROM DICTIONARY BEFORE ITERATING OVER IT AND REPLACING VALUES
		# NVM, actually just have a check for if the label isn't in the array ----- Just dn'don't do anything

print "Var assignments removed\n", secondInstrList, "\n" , len(secondInstrList), " instructions conuted"
print "Varibale Map Too: ", variables


print "----"
""" Removing tabs, spaces, new lines and special characters"""
for i in range(len(secondInstrList)):
	secondInstrList[i] = re.sub('[^A-Za-z0-9]+', ' ', secondInstrList[i])

print "Special Characters removed\n", secondInstrList, "\n"


for i in secondInstrList:
	instruction = i
	if i == ' ':
		instruction = ''
	thirdInstrList.append(instruction)

thirdInstrList = filter(None, thirdInstrList)
print "Empty Strings removed\n", thirdInstrList, "\n", len(thirdInstrList), " instructions conuted"

for i in range(len(thirdInstrList)):
	fourthInstrList.append(thirdInstrList[i].strip())

print "Ready for splitting!\n", fourthInstrList, "\n", len(fourthInstrList), " instructions conuted"




for i in range(len(fourthInstrList)):
	finalInstrList.append(fourthInstrList[i].split(" "))

print "Split!\n", finalInstrList, "\n", len(finalInstrList), " instructions conuted"


print "----"
""" Make 2D Array of Each Instruction"""
for varName, varValue in variables.iteritems():
	print "current var, ", varName
	counter = variables["labelBase"]
	for i in range(len(finalInstrList)):
		counter += 1
		if varName in finalInstrList[i]:
			if varValue == 0:
				varValue = str(counter) #SHOULD I ONLY PASS YOU INTS ?    <-------
			labelIndex = finalInstrList[i].index(varName)
			print "var here, value here", varName, varValue
			finalInstrList[i][labelIndex] = finalInstrList[i][labelIndex].replace(varName, varValue)

print "Done.", finalInstrList, "\n"




specialInstr = ['.ORIG','.WORD','.NAME']

alu_r_list = ['ADD','SUB','AND','OR','XOR','NAND','NOR','XNOR']
alu_r_dict ={'ADD':'00111111','SUB':'00101111','AND':'01111111' ,'OR':'01101111','XOR':'01011111','NAND':'10111111','NOR':'10101111','XNOR':'10011111'}

alu_i_list = ['ADDI','SUBI','ANDI','ORI','XORI','NANDI','NORI','XNORI','MVHI']
alu_i_dict = {'ADDI':'00111011','SUBI':'00101011','ANDI':'01111011','ORI':'01101011','XORI':'01011011','NANDI':'10111011','NORI':'10101011','XNORI':'10011011','MVHI':'11111011'}

lw_sw_list = ['LW','SW']
lw_sw_dict = {'LW':'00001000','SW':'00001001'}

cmp_r_list = ['F','EQ','LT','LTE','T','NE','GTE','GT']
cmp_r_dict = {'F':'00111110','EQ':'11001110','LT':'11011110','LTE':'00101110','T':'11111110','NE':'00001110','GTE':'00011110','GT':'11101110'}

cmp_i_list = ['FI','EQI','LTI','LTEI','TI','NEI','GTEI','GTI']
cmp_i_dict = {'FI':'00111010','EQI':'11001010','LTI':'11011010','LTEI':'00101010','TI':'11111010','NEI':'00001010','GTEI':'00011010','GTI':'11101010'}

br_notZ_list = ['BF','BEQ','BLT','BLTE','BT','BNE','BGTE','BGT']
br_Z_list = ['BEQZ','BLTZ','BLTEZ','BNEZ','BGTEZ','BGTZ']

br_dict = {'BF':'00110000','BEQ':'11000000','BLT':'11010000','BLTE':'00100000','BEQZ':'10000000','BLTZ':'10010000','BLTEZ':'01100000','BT':'11110000'
			,'BNE':'00000000','BGTE':'00010000','BGT':'11100000','BNEZ':'01000000','BGTEZ':'01010000','BGTZ':'10100000'}

jal = 'JAL'
jal_dict = {'JAL':'00000001'}

pseudo_list = ['BR', 'NOT', 'BLE','BGE','CALL','RET','JMP'] 

reg_dict = {'R0':'0000','R1':'0001','R2':'0010','R3':'0011','RV':'0011','A0':'0000','A1':'0001','A2':'0010','A3':'0011','R4':'0100','R5':'0101',
			'T0':'0100','T1':'0101','R6':'0110','R7':'0111','R8':'1000','S0':'0110','S1':'0111','S2':'1000', 'R9':'1001','R10':'1010','R11':'1011','R12':'1100', 
			'GP':'1100','R13':'1101','FP':'1101','R14':'1110','SP':'1110','R15':'1111', 'RA':'1111'}

currAddr = -1


def readAssembly(assembly):

	# this is for the beginning for the mif file
	beginning ='DEPTH = 32;\nDEPTH=2048;\nADDRESS_RADIX = HEX;\nDATA_RADIX = BIN;\nCONTENT BEGIN;\n[00000000..0000000f] : DEAD;\n'
	outputFile.write(beginning)

	global currAddr
	


	for instrList in assembly:
		instr = '' #ADDED THIS LINE                   <--------------------
		currAddr += 1
		opcode = instrList[0]
		operands = instrList[1:]

		if opcode in specialInstr:

			if opcode == '.WORD':
				instr = special_instr(opcode,operands)
				mifLine = format(currAddr ,'08x') + ' : ' + instr+ ';' + '\n'
				outputFile.write(mifLine)

			elif opcode == '.ORIG':
				special_instr(opcode,operands)

			else:
				special_instr(opcode,operands)
		
		else:

			if opcode in pseudo_list:
				

				if opcode == 'BR':
					instr = pseudo_br_op(opcode,operands)
					mifLine = format(currAddr ,'08x') + ' : ' + instr+ ';' + '\n'
					outputFile.write(mifLine)

				elif opcode == 'NOT':
					instr = pseudo_not_op(opcode,operands)
					mifLine = format(currAddr ,'08x') + ' : ' + instr+ ';' + '\n'
					outputFile.write(mifLine)

				elif opcode == 'BLE' or opcode == 'BGE':
					instrTuple = pseudo_ble_bge_op(opcode,operands)

					instr = instrTuple[0]
					mifLine = format(currAddr ,'08x') + ' : ' + instr+ ';' + '\n'
					outputFile.write(mifLine)

					lineNum += 1
					instr = instrTuple[1]
					mifLine += format(currAddr ,'08x') + ' : ' + instr+ ';' + '\n'
					outputFile.write(mifLine)


				else:
					instr = pseudo_call_ret_jmp(opcode,operands)
					mifLine = format(currAddr ,'08x') + ' : ' + instr+ ';' + '\n'
					outputFile.write(mifLine)

			else:
				if opcode in alu_r_list:
					instr = alu_r_op(opcode,operands)
				elif opcode in alu_i_list:
					instr = alu_i_op(opcode,operands)
				elif opcode in lw_sw_list:
					instr = lw_sw_op(opcode,operands)
				elif opcode in cmp_r_list:
					instr = comp_r_op(opcode,operands)
				elif opcode in cmp_i_list:
					instr = comp_i_op(opcode,operands)
				elif opcode in br_notZ_list:
					instr = br_notZ_op(opcode,operands)
				elif opcode in br_Z_list:
					instr = br_Z_op(opcode,operands)
				elif opcode == jal:
					instr = jal_op(opcode,operands)


				mifLine = format(currAddr ,'08x') + ' : ' + instr+ ';' + '\n' 
				print(currAddr)
				outputFile.write(mifLine)

	# writing the mifLine to mif file

	ending = 'END;'
	outputFile.write(ending)	
	outputFile.close()

def alu_r_op(opcode, operands):
	instr = ''
	opcodeBits = alu_r_dict[opcode]
	
	rs2 = operands[0]
	rs1 = operands[1]
	rd = operands[2]

	rs2Bits = reg_dict[rs2]
	rs1Bits = reg_dict[rs1]
	rdBits = reg_dict[rd]

	if (opcodeBits != None) and (rs2Bits != None) and (rs1Bits != None) and (rdBits != None):
		instr += opcodeBits + format(0,'012b') + rs2Bits + rs1Bits + rdBits
	return instr 

def alu_i_op(opcode, operands):
	# need to take labels into account 
	instr = ''

	if opcode == 'MVHI':
		opcodeBits = alu_i_dict[opcode]

		if "0x" in operands[0]:
			imm = int(operands[0], 0)
		else:
			imm = int(operands[0])
		rd = operands[1]

		immBits = format(imm, '016b')
		rdBits = reg_dict[rd]
		
		if (opcodeBits != None) and (immBits != None) and (rdBits != None):
			instr += opcodeBits + immBits + format(0,'04b') + rdBits
			return instr
	else:		
		opcodeBits = alu_i_dict[opcode]
		
		if "0x" in operands[0]:
			imm = int(operands[0], 0)
		else:
			imm = int(operands[0])
		rs1 = operands[1]
		rd = operands[2]

		immBits = format(imm, '016b')
		rs1Bits = reg_dict[rs1.upper()]
		rdBits = reg_dict[rd.upper()]

		if (opcodeBits != None) and (immBits != None) and (rs1Bits != None) and (rdBits != None):
			instr += opcodeBits + immBits + rs1Bits + rdBits
	return instr 

def lw_sw_op(opcode, operands):
	instr = ''
	
	opcodeBits = lw_sw_dict[opcode]

	if "0x" in operands[0]:
		imm = int(operands[0], 0)
	else:
		imm = int(operands[0])
	rs1 = operands[1]
	reg2 = operands[2]

	immBits = format(imm, '016b')
	rs1Bits = reg_dict[rs1]
	reg2Bits = reg_dict[reg2]

	if (opcodeBits != None) and (immBits != None) and (rs1Bits != None) and (reg2Bits != None):
		if opcode == 'LW':
			instr += opcodeBits + immBits + rs1Bits + reg2Bits
		else:
			instr += opcodeBits + immBits + reg2Bits + rs1Bits
	return instr

def comp_r_op(opcode, operands):
	instr = ''
	opcodeBits = comp_r_dict[opcode]
	
	rs2 = operands[0] 
	rs1 = operands[1]
	rd = operands[2]

	rs2Bits = reg_dict[rs2]
	rs1Bits = reg_dict[rs1]
	rdBits = reg_dict[rd]

	if (opcodeBits != None) and (rs2Bits != None) and (rs1Bits != None) and (rdBits != None):
		instr += opcodeBits + format(0,'012b') + rs2Bits + rs1Bits + rdBits

def comp_i_op(opcode,operands):
	instr = ''
	opcodeBits = comp_i_dict[opcode]
	
	imm = int(operands[0]) 
	rs1 = operands[1]
	rd = operands[2]

	immBits = format(imm, '016b')
	rs1Bits = reg_dict[rs1]
	rdBits = reg_dict[rd]

	if (opcodeBits != None) and (immBits != None) and (rs1Bits != None) and (rdBits != None):
		instr += opcodeBits + immBits + rs2Bits + rs1Bits + rdBits

	return instr

def br_notZ_op(opcode,operands):
	instr = ''
	opcodeBits = br_dict[opcode]

	imm = int(operands[0])
	rs2 = operands[1]
	rs1 = operands[2]

	immBits = format(imm, '016b')
	rs2Bits = reg_dict[rs2]
	rs1Bits = reg_dict[rs1]

	if (opcodeBits != None) and (immBits != None) and (rs2Bits != None) and (rs1Bits != None):
		instr += opcodeBits + immBits + rs2Bits + rs1Bits

	return instr

def br_Z_op(opcode,operands):
	instr = ''
	opcodeBits = opcodeBits = br_dict[opcode]

	imm = int(operands[0])
	rs1 = operands[1]

	immBits = format(imm,'016b')
	rs1Bits = reg_dict[rs1]

	if (opcodeBits != None) and (immBits != None) and (rs1Bits != None):
		instr += opcodeBits + immBits + format(0,'04b') + rs1Bits

	return instr

def jal_op(opcode,operands):
	instr = ''
	opcodeBits = jal_dict[opcode]
	
	imm = int(operands[0]) 
	rs1 = operands[1]
	rd = operands[2]

	immBits = format(imm, '016b')
	rs1Bits = reg_dict[rs1]
	rdBits = reg_dict[rd]

	if (opcodeBits != None) and (immBits != None) and (rs1Bits != None) and (rdBits != None):
		instr += opcodeBits + immBits + rs1Bits + rdBits

	return instr

def pseudo_br_op(opcode,operands):
	
	imm = int(operands[0])
	
	return br_notZ_op('BEQ',[imm,'R6','R6'])		

def pseudo_not_op(opcode,operands):
	
	rs = operands[0]
	rd = operands[1]

	return alu_r_op('NAND',[rs,rs,rd])

def pseudo_ble_bge_op(opcode,operands):
	instr = ''

	imm = int(operands[0])
	rs2 = operands[1]
	rs1 = operands[2]

	if opcode == 'BLE':
		instr = (br_notZ_op('LTE',[rs2,rs1,'R6']), br_Z_op('BNEZ',[imm,'R6']))
	else:
		instr = (br_Z_op('GTE',[rs2,rs1,'R6']), br_Z_op('BNEZ',[imm,'R6']))

	return instr

def pseudo_call_ret_jmp(opcode,operands):
	instr = ''

	if opcode == 'CALL':
		imm = int(operands[0])
		rs1 = operands[1]

		return jal_op('JAL', [imm,rs1,'RA'])

	elif opcode == 'RET':
		return jal_op('JAL', [0,'RA','R9'])
	
	else:
		imm = int(operands[0])
		rs1 = operands[1]

		return jal_op('JAL',[imm,rs1,'R9'])		

def special_instr(opcode,operands):

	if opcode == '.NAME':

		return
	
	elif opcode == '.ORIG':
		global currAddr
		currAddr = int(operands[0],16)/4
		return
	
	else:
		return operands[0]


   
test = [['MVHI', '8192', 'SP'],['ADDI', '8192', 'SP', 'SP'],['ANDI', '0', 'S0', 'S0'],['SW', '0', 'T0', 'S1'],['RET']]

readAssembly(finalInstrList)


outputFile.close()
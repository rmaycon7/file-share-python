# coding: utf8
'''
inicio do programa cliente
# Maycon de Arruda Rebordão
# Jhuan Victor 
# Dia 12/10/2016 Formosa - GO
# Usuario do servidor : Best_Files
# name: Best_Downs
'''
''' biblioteca para funcao basicas como manipulacao de arquivos e diretorios	'''
import os 		
''' biblioteca com os tipos de sockets ja predefinidos do python '''
import socket 
''' biblioteca para acessar e executar funcoes relacionadas ao relogio do computador '''
import time		
''' bibliteca de threads, funcoes de multitarefas '''
import _thread 			
import sys
'''permite o uso de funcoes basicas como pegar o tamanho de um arquivo ou limpar a tela'''
from datetime import datetime
from os import system


# funcao para contar quantos diretorios tem na pasta


# def countDirectories():
	# print("sd")



'''
funcao para deletar arquivos
'''
def delet_file(j):
	try:
		os.remove(j)
		return True
	except Exception as e:
		return False
'''
funcao para deletar a pasta tmp apos a execucao do programa
'''
def dele_tmp():
	try:
		dire = os.getcwd()
		pasta = '%s/.tmp_clt'%dire
		lista = os.listdir(pasta)
		i = get_siz(lista)
		for j in range(i):
			if delet_file('%s'%pasta+'/%s'%lista[j]) == True: j += 0
			else: j-=1
		os.rmdir(pasta)
		return True
	except Exception as e:
		return False
'''
funcao para deletar a pasta e os arquivos baixados
'''
def dele_dowlaod():
	try:
		pasta = get_fodler()
		lista = os.listdir(pasta)
		i = get_siz(lista)
		for j in range(i):
			if delet_file('%s'%pasta+'/%s'%lista[j]) == True: j += 0
			else : j -= 1 
		return True
	except Exception as e:
		return False
'''
funcao para salvar a lista de arquivos baixados
'''
def save_list_file_recive():
	lista = os.listdir(get_fodler())
	lista.sort()
	file = open(make_folder_tmp_clt('list_of_file_recive.r'),'w')
	if len(lista) == 0:
		return 0
	for i in range(len(lista)):
		file.write(lista[i]+"\n")
	return True
'''
funcao para imprimir a lista de arquivos baixados
'''
def print_recive():
	save_list_file_recive()
	file  = open(make_folder_tmp_clt('list_of_file_recive.r'),'r')
	lista = file.readlines()
	if get_siz(lista) == 0:
		print("\tPasta De Arquivos Baixados Esta Vazia!")
		pausa(3)
		limpa()
		return 0
	print("\t\tTodos os Arquivo(s) já baixado(s).\n")
	for i in range(len(lista)):
		print("\t%d- "%i+lista[i])
	return len(lista)
'''
funcao para retornar o nome e o caminho do arquivo que esta na lista de arquivos recebidos
para que ele seja excluido
'''
def file_recive(k):
	file = open(make_folder_tmp_clt('list_of_file_recive.r'),'r')
	lista = file.readlines()
	return get_fodler()+'/%s'%lista[k][:len(lista[k])-1]
'''
funcao que imprimi a lista de arquivos disponiveis
'''
def print_list():
	limpa()
	file = open(make_folder_tmp_clt('lista_de_arquivos.cl'),'r')
	lista = file.readlines()
	if len(lista) == 0:
		print("\tlista vazia!")
	else:
		print("\t\t Lista Ordenada De Modo:")
		print("\t\t 0-9 e &$# e A-Z e a-z\n")	
		for i in range(len(lista)):
			print("\t%d- "%i+lista[i])
	file.close()
	return len(lista)
'''
funcao para criar a lista em uma pasta oculta do usuario
e funcao que cria a pasta temporaria que o programa usa durante 
a execucao, que so e oculta no linux
'''
def make_folder_tmp_clt(j):
	dire = os.getcwd()
	try:
		folder = os.mkdir('%s/.tmp_clt'%dire)
		return folder+'/%s'%j
	except Exception as e:
		folder = '%s/.tmp_clt'%dire
		return folder+'/%s'%j
'''
funcao que serve para pegar o tamanho da lista de arquivos disponiveis
ela retorna um inteiro
'''
def get_size_list():
	file = open(make_folder_tmp_clt('lista_de_arquivos.cl'),'r')
	lista = file.readlines()
	file.close()
	return int(len(lista))
'''
funcao que recebe a lista de arquivos disponiveis para download, 
para o cliente
'''
def recive_list(con, size):
	'''
	aqui o clinte se conecta na segunda conexao com o servidor 
	para fazer o download do arquivo previamente selecionado pelo cliente
	abrindo arquivo de texto para salvar a lisat de arquivos 
	'''
	lista = open(make_folder_tmp_clt('lista_de_arquivos.cl'),'wb',buffering = -1, encoding = None)
	tmp = 0
	''' laco de recebimento da lista  '''
	while tmp < size:
		try:
			dado = con.recv(1024)
		except Exception :
			dele_tmp()
			con.close()
			limpa()
			print("\tServidor inalcansavel no momento.")
			print("\n\tCliente Desligado")
			os._exit(3)		 
		tmp += len(dado)
		lista.write(dado)
	lista.close()
	'''
	chamando a funcao que imprime na tela a lista de arquivos
	'''
	print_list()
	return 0
'''
criando uma pasta com a data atual

'''

def takeDAte():
	data = datetime.now()
	dia  = data.day
	mes = data.month
	ano = data.year

	return "%s-%s-%s"%(dia,mes,ano)


'''
funcao que verifica se ja existe a pasta para salvar os arquivos 
que sao recebidos nos downloads, e caso eles nao existam ela cria uma pasta nova
'''
def if_folder_exist():
	dire = os.getcwd()
	data = takeDAte()


	try:
		'''
		tentando criar a pasta para salvar os arquivos que seram baixados
		'''
		
		os.mkdir('%s/Files-%s'%(dire,data))
		return False
	except Exception:
		''' 
		caso nao consiga criar a pasta e porque ela 
		ja existe
		'''
		return True
'''
retorna a pasta para salvar os arquivos recebidos
'''
def get_fodler():
	data = takeDAte()	 
	'''
	retornando o enderecao da pasta de downloads de arquivos
	'''
	return '%s/Files-%s'%(os.getcwd(),data)
'''
funcao que retorna o nome do arquivo que sera recebido pelo cliente
'''
def get_name(j):
	'''
	abrindo a lista de arquivos para selecionar o nome do arquivo
	que sera baixado
	'''
	file = open(make_folder_tmp_clt('lista_de_arquivos.cl'),'r')
	lista = file.readlines()
	'''
	retornando o nome do arquivo que sera recebido
	'''
	return lista[j][:len(lista[j])-1]
'''
funcao que decodifica e retorna um inteiro de msg recebida
'''
def get_siz(l):
	return int(len(l))
'''
funcao para limpar a tela
'''
def limpa():
	''' 
	funcao que limpa a tela tanto no windows quanto no linux
	'''
	os.system('cls' if os.name == 'nt' else 'clear')
	return 0
'''
funcoes para pausar a execusao do programa por alguns instantes
'''
def pausa(k):
	''' pausando a execucao do programa por k segundo '''
	time.sleep(k)
	return 0
'''
funcao para verificar se o arquivo foi aberto com sucesso
'''
def try_open(nome):
	try:
		pasta = get_fodler()
		file  = open('%s'%pasta+'/%s'%nome,'wb',buffering = -1, encoding = None)
		file.close()
		return 1
	except Exception as e:
		return 0
'''
funcao para receber o arquivo selecionado pelo cliente
'''
def recive_file(con, size, j):
	'''
	size recebe o tamanho do arquivo que sera recebido
	pegando o endereço onde o cliente salvara os arquivos baixados
	'''
	pasta = get_fodler()	
	'''
	chamada da funcao que retorna o no do arquivo que vai ser salvo
	'''
	nome = get_name(j)
	a = try_open(nome)
	if a == 0:
		print("\tERRO ao abrir arquivo!!!")
		pausa(3)
		limpa()
		return 0	
	elif size == 0:
		limpa()
		arq = open('%s'%pasta+'/%s'%nome,'wb',buffering = -1,encoding = None)
		arq.close()
		print("\tBaixando... %.2f %% Recebido. \n\t"%100+"[%s]"%bar(100))
		pausa(2)
		limpa()
		return 0
	file = open('%s'%pasta+'/%s'%nome,'wb',buffering = -1,encoding = None)
	buff = 0
	tmp = buff
	if size> 13107200:
		buff = int(size/100)
	else:
		buff = 131072
	'''
	iniciando o recebimento do arquivo
	'''
	limpa()
	print("\n\n\n\n\t%s\n\tBaixando..."%nome)
	while tmp < size:
		try:
			dado = con.recv(buff)
		except Exception :
			dele_tmp()
			con.close()
			limpa()
			print("\tServidor inalcansavel no momento.")
			print("\n\tCliente Desligado")
			os._exit(3)
		tmp += len(dado)
		file.write(dado)
		# limpa()
		parcial = float(100*(tmp/size))
		# print("\n\n\n\n\n\n\n\n\n\t%s"%nome)
		# print("\tBaixando... %.2f %% Recebido. \n\t"%parcial+"[%s]"%bar(parcial))
		sys.stdout.write('\t[%s] %.2f%%\r' % (bar(parcial),parcial))
		sys.stdout.flush()
	'''
	fim do recebimento
	'''
	pausa(2)
	file.close()
	limpa()
	return 0
'''
funcao que cria a barra de download completo, ela retorna a barra proporcionalmente 
a porcentagem completada do download
'''
def bar(n):
	l = ""	
	for i in range(int(n/2)):
		l+="#"
	g = ((100 - n)/2)+1
	if n == 100:
		return l
	for i in range(int(g)):
		l+=" "
	return l
'''
funcao que cria o socket de conexao entre cliente e servidor
conexao 1
'''
def make_socket(porta2, i, ip):
	i = 0
	'''
	laco que tenta estabelecer a conexao por cinco vezes consecutivas
	caso nao obtenha sucesso, ele se encerra e retorna 0, para avisar
	que nao houve sussesso no estabelecimento de conexao, nessas 
	tentativas a porta de conexao muda juntamente com a porta usada pelo cliente tambem
	'''
	while True:
		try:
			conect1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			conect1.connect((ip,porta2))
			return conect1
		except Exception as e:
			porta2+=1			
			if i == 5:
				break
			i+=1
	return 0
'''
funcao para tentar iniciar a conexao com o servidor 
caso nao consiga de primeira ele tenta ate conseguir 
'''
def make(con, porta2, ip):
	'''
	laco que se repete enquanto nao for estabelecida uma conexao
	'''
	while con == 0:
		con = make_socket(porta2,0,ip)
	return con
'''
funcao que envia uma msg de erro para finalizar a execusao o servidor e do cliente caso 
seja encontrado algum erro ou em caso de muitas repeticoes de opcoes erradas 
no programa
'''
def error(con):
	try:
		msg = "end"
		con.send(msg.encode())
		con.close()
		return True
	except Exception as e:
		dele_tmp()
		con.close()
		limpa()
		print("\tServidor inalcansavel no momento.")
		print("\n\tCliente Desligado")
		os._exit(3)
'''
funcao para verificar se o IP fornecido pelo o usuario e um IP valido
'''
def ip_valido(ip):
	a = ip.split('.')
	i = int(len(a))
	'''
	verificando se o IP fornecido possui quatro ".", para seer considerado um formato de IP valido
	'''
	if i <4:
		return 0
	return 1
'''
funcao para salvar o valor no arquivo de verificacao de erro
'''
def save_status(a):
	'''
	salva sempre o valor "a" que ela recebe no arquivo "errro.tmp" na pasta ".tmp_clt"
	'''
	file = open(make_folder_tmp_clt('erro.tmp'),'w')
	file.write(a)
	file.close()
	return 0
'''
funcao para verificar o tempo de tentativa de estabelecimento de conexao com o servidor
para evitar que o programa fique em um loop infinito tentando se conectar com o servidor
'''
def loop():
	pausa(15)
	'''
	caso no periodo de 8 segundos nao seja possivel estabelecer uma conexao com o servidor o pragrama aborta sua conexao
	'''
	if verifica() == 1:
		limpa()
		print("Endereco de IP nao alcansado!! Encerrando a execussao, Tente novamente com um IP certo.")
		dele_tmp()
		os._exit(3)
		return 0
'''
funcao que retorna o valor salvo no arquivo de verificacao de erro de conexao
'''
def verifica():
	file  = open(make_folder_tmp_clt('/erro.tmp'),'r')
	erro = file.readlines(1)
	file.close()
	return int(erro[0])
'''
funcao para receber o tamanho do arquivo que sera enviado pelo servidor 
'''
def recive_size(con):
	try:
		msg = con.recv(1024)
		size  = int(msg.decode())
		return size
	except Exception :
		dele_tmp()
		con.close()
		limpa()
		print("\tServidor inalcansavel no momento.")
		print("\n\tCliente Desligado")
		os._exit(3)
'''
opcao A(funcao para receber a lista de arquivos disponiveis no servidor)
'''
def op_a(con):
	erro = 0
	try:
		msg = "a"
		con.send(msg.encode())
		erro = False
	except Exception :
		erro = True	
	size = recive_size(con)
	msg = "ok"
	try:
		con.send(msg.encode())
		erro = False
	except Exception :
		erro = True
	if size == 0:
		print("Lista de arquivos vazia!")
		pausa(2)
		limpa()
		return 0
	if erro == True:
		dele_tmp()
		con.close()
		limpa()
		print("\tServidor inalcansavel no momento.")
		print("\nCliente Desligado")
		os._exit(3)
	recive_list(con, size)
	return True

	
'''
funcao para enviar o indece do arquivo solicitado pelo cliente
'''
def send_indice(con,i):
	try:
		msg = str(i)
		con.send(msg.encode())
		return True
	except Exception as e:
		dele_tmp()
		con.close()
		limpa()
		print("\tServidor inalcansavel no momento.")
		print("\nCliente Desligado")
		os._exit(3)
'''
opcao B (funcao para receber o arquivo que o servidor enviara)
'''
def op_b(con,i):
	try:
		msg = "b"
		con.send(msg.encode())
		msg = con.recv(1024)
		send_indice(con,i)
		size  = recive_size(con)
		msg = "ok"
		con.send(msg.encode())
		recive_file(con, size, i)
		return True
	except Exception as e:
		dele_tmp()
		con.close()
		limpa()
		print("\tServidor inalcansavel no momento.")
		print("\nCliente Desligado")
		os._exit(3)
'''
funcao para o usuario escolher o arquivo que sera baixado
'''
def escolha(i):
	while True:
		limpa()
		print_list()
		print("\n\t|===============================|")
		opcao = input("\t|Escolha Um Arquivo\t\t|\n\t|===============================|\n\t|Digite o indice do arquivo ou\t|\n\t|Digite \"V\" Para Voltar Ao Menu :\t")
		'''  verificando se a opcao selecionada esta correta  '''
		try:
			if int(opcao) <0 :
				limpa()
				print("\tOpcao Errada!")
				pausa(3)
			elif int(opcao)>=i:
				limpa()
				print("\tOpcao Errada!")
				pausa(3)
				''' 	caso ele entre no else significa que a opcao selecionada esta correta '''
			else:break
			''' se nao conseguir verificar o tamanho da opcao, se ele nao fom um inteiro
			significa que foi digitado um caractere ao invez de um numero.
			'''
		except Exception:
			if opcao == "v" or opcao == "V":
				limpa()
				return opcao				
			limpa()
			print("\tOpcao Errada!. Digite Numero, Nao um Caractere!")
			pausa(3)
	return int(opcao)
'''
funcao que retorna o indice do arquivo escolhido pelo usuario para ser excluido.
'''
def escolha_recive():
	while True:
		limpa()
		k =	print_recive()
		if k == 0:
			return -1
		print("\n\t#=======================================================#")
		print("\t#\tDigite De Um Arquivo Para Ser Excluido:\t\t#")
		print("\t#\tDigite \"B\" para voltar ao menu principal.\t#")
		a = input("\t#=======================================================#\t")
		try:
			if int(a) <0 :
				limpa()
				print("\tOpcao Errada!")
				pausa(3)
			elif int(a)>k-1:
				limpa()
				print("\tOpcao Errada!")
				pausa(3)
			else:break
		except Exception:
			if a == "b" or a == "B":
				limpa()
				return a				
			limpa()
			print("\tOpcao Errada!. Digite Numero, Nao um Caractere!")
			pausa(3)
	return int(a)
'''
opcao (D) funcao para excluir um arquivo selecionado pelo cliente
'''
def op_d():
	while True:
		op = escolha_recive()
		if op == -1:
			return True
		if op == "b" or op == "B":
			return True
		delet_file(file_recive(op))
'''
funcao que imprime o menu na tela
'''
def print_menu():
	print("\n\t#=======================================================#")
	print("\t# Escolha Uma Opcao:\t\t\t\t\t#")
	print("\t# \tA - Para Listar Arquivos.\t\t\t#")
	print("\t# \tB - Para Baixar Um Arquivo.\t\t\t#")
	print("\t# \tC - Apagar todos arquivos baixados.\t\t#")
	print("\t# \tD - Apagar Um Arquivo Baixado.\t\t\t#")
	print("\t# \tE - Visualizar Lista de Arquivos Já Baixados.\t#")
	print("\t# \tL - limpar tela.\t\t\t\t#")
	print("\t# \tT - Para Baixar Todos os Arquivos.\t\t#")
	print("\t# \tS - Sair.\t\t\t\t\t#")
	print("\t#=======================================================#")
	op = input("\t#\tDigite a opcao: ")
	return op
'''
funca que cerifica se a conexao estabelecida foi com o servidor original
'''
def conect_verify(con):
	msg = "ok_madara"
	con.send(msg.encode())
	msg = con.recv(1024)
	if msg.decode() == "IO_Tensei":
		return True
	else:
		return False
'''
main
'''
while True:
	''' chamando a funcao de verificacao de existencia ou nao da pasta reservada para download de arquivos '''
	if_folder_exist()
	erro = 0
	porta2 = 8080
	ip = ''
	'''
	laco  para forcar o usuario a digitar um IP no formato certo
	'''
	while not ip_valido(ip):
		ip = input("\n\tDigite o IP Do Servidor: Exemplo \"127.0.0.1\":\t")
		if ip == '' or ip == ' ':
			ip = '127.0.0.1'
		if ip_valido(ip)== 0:
			limpa()
			print("IP invalido!")
			pausa(2)			
	save_status('1')
	''' a thread que ficara rodando para verificar o tempo que o cliente esta
	tentando estabelecer a conexao
	'''
	_thread.start_new_thread(loop, tuple([]))
	''' tentando a conexao '''
	conect1 = make (make_socket(porta2,0,ip),porta2,ip)
	save_status('1')
	if conect_verify(conect1) == False:
		erro = 10
		print("\tServidor Nao reconhecido.")
		pausa(3)
		limpa()
		print("\tCliente Desligado.")			
		''' deletando a pasta de arquivos temporarios	'''
		dele_tmp()
		'''enxerrando a conexao com o servidor '''
		conect1.close()
		break
	save_status('0')
	cont1 = 0
	limpa()
	'''
	laco do programa servidor, que so se encerrar caso seja selecionada opcao sair ou
	que seja feita muitar tentativas erradas repetidas
	'''
	while True:
		if erro == 10:
			limpa()
			print("\t\nMuitas Tentativas Erradas...\n\tCliente Desligado.")
			pausa(3)
			error(conect1)
			break
		op = print_menu()
		if op == "a" or op == "A":
			erro = 0
			''' 
			chamando a funcao que se comunica com o servidor para fazer o donwload da lista de arquivos
			faz parte do protocolo 
			adotado na criacao desse programa
			'''
			op_a(conect1)
		elif op == "b" or op == "B":
			''' 
			para ganrantir que a lista nao sofra nenhuma alteracao manual 
			e pedida uma nova lista a cada vez que o cliente seleciona baixar um arquivo novo
			'''
			op_a(conect1)	
			''' 
			recebendo o tamanho da lista 
			'''
			i = get_size_list()
			'''
			funcao responsavel por permitir e garantir que o usuario escolha 
			um arquivo para download, e que esse aruivo esteja na lista
			'''
			a = escolha(i)
			erro = 0				
			if a == "v":
				erro = 0
			else:
				op_b(conect1, a)			
		elif op == "c" or op == "C":
			limpa()
			d = input("\tTem Certeza que Deseja Apagar todos Os Arquivos Baixados? [S/N]\t")
			if d == "S" or d == "s":
				dele_dowlaod()
				limpa()
				print("\tTodos os Arquivos Apagados")
				pausa(1)
			limpa()
			erro = 0
		elif op == "d" or op == "D":
			'''
			chmando a funcao que permite ir apagando arquivos por arquivo 
			assim o ususario pode escolher quais arquivos quer excluir, dos arquivos que ja foram baixados.
			'''
			op_d()
		elif op == "e" or op == "E":
			limpa()
			'''
			chamando a funcao que ira imprimir na tela a lista conetndo todos os arquivos que ja foram baixados pelo usuario.
			'''
			print_recive()
		elif op =="l" or op == "L":
			''' apenas limpando a tela '''
			limpa()
			erro  = 0
		elif op == 'T' or op == 't':
			op_a(conect1)	
						
			erro = 0				
			
			i = 0
	
			for i in range (get_size_list()):

				op_b(conect1, i)
			

		elif op == "s" or op == "S":
			''' enviando opcao de encerramento de execucao 
			'''
			msg = "s"
			conect1.send(msg.encode())
			erro = 10
			limpa()
			print("\tCliente Desligado.")			
			break
		else:
			limpa()
			print("\tOpcao Errada!")
			pausa(2)
			limpa()
			erro += 1
	''' 
	encerrando execuacao do cliente
	'''
	if erro == 10:
		''' deletando a pasta de arquivos temporarios	'''
		dele_tmp()
		'''enxerrando a conexao com o servidor '''
		conect1.close()
		break
'''
fim  do programa cliente
'''
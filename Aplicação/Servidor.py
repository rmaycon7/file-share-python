'''
inicio do programa servidor
# Jhuan Victor
# Maycon de Arruda Rebordão
# Dia 12/10/2016
# Servidor de Arquivos
# nome: Best_Files
'''
import os
import socket
import time
import _thread
import zipfile
import sys
import string
from os import system

'''
funcoes para pausar a execusao do programa por alguns instantes
'''


def pausa(k):
	''' pausando a execucao do programa por k segundo '''
	time.sleep(k)
	return 0
'''
funcao para deletar arquivos
'''


def delet_file(j):
	try:
		os.remove(j)
		return 0
	except Exception as e:
		return 0
'''
funcao para deletar a pasta tmp apos a execucao do programa
'''


def dele_tmp():
	try:
		dire = os.getcwd()
		pasta = '%s/.tmp_srv' % dire
		for root, dirs, files in os.walk(raiz, topdown=False):
			for name in files:
				try:
					os.remove(os.path.join(root, name))
				except Exception as e:
					# raise e
					pass
				# print(os.path.join(root, name))
			for name in dirs:
				try:
					os.rmdir(os.path.join(root, name))
				except Exception as e:
					pass
					# raise e
				# print(os.path.join(root, name))
		return 0
	except Exception as e:
		return 0
'''
funcao para criar a lista em uma pasta oculta do usuario
'''


def make_folder_tmp_srv(j):
	dire = os.getcwd()
	try:
		folder = os.mkdir('%s/.tmp_srv' % dire)
		return folder + '/%s' % j
	except Exception as e:
		folder = '%s/.tmp_srv' % dire
		return '%s' % folder + '/%s' % j
'''
pega a lista de arquivos na pasta e retornar ele
'''


def get_list():
	return os.listdir(os.getcwd())
'''
funcao para verificar se o nome do arquivo pode ser salvo na lista
'''


def _valido(n):
	try:
		file = open(n, 'rb', buffering=-1, encoding=None)
		file.close()
		return 0
	except Exception as e:
		return 1
'''
funcao que retorna o inteiro do tamanho da lista
'''


def get_siz(l):
	return int(len(l))
'''
enviar a lista de arquivos que o servidor tem disponiveis
para download
'''


def save_list():
	l = get_list()
	''' ordenando a lista de Arquivos'''
	l.sort()
	i = 0
	j = get_siz(l)
	file = open(make_folder_tmp_srv('lista_de_arquivos.s'), 'w')
	while i < j:
		k = l[i]
		''' verificando se o nome do arquivo pode ser salvo na lista '''
		if _valido(k) == 0:
			file.write(k + "\n")
		i += 1
	file.close()
	return 0
'''
funcao que retorna a lista de arquivos disponiveis salva
'''


def get_list_saved():
	file = open(make_folder_tmp_srv('lista_de_arquivos.s'), 'r')
	lista = file.readlines()
	return lista
'''
funcao para enviar a lista de arquivos disponiveis para download pelo cliente
'''


def send_list(con):
	save_list()
	lista = open(make_folder_tmp_srv('lista_de_arquivos.s'),
				 'rb', buffering=-1, encoding=None)
	size = os.stat(make_folder_tmp_srv('lista_de_arquivos.s')).st_size
	tmp = 0
	while tmp < size:
		try:
			dado = lista.read(1024)
			tmp += len(dado)
			con.send(dado)
		except Exception as e:
			return False

	print("\tLista Enviada!")
	return True
'''
funcao para zerar os bytes de um arquivo, que ele recebe
'''


def zero_file(j):
	file = open(j, 'wb')
	file.close()
	return 0
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
funcao que retorna a localizao onde o programa esta sendo excutado
'''


def get_folder():
	return os.getcwd()
'''
funcao para pegar o nome do arquivo que sera enviado
para pegar o nome do arquivo que sera enviado
'''


def get_file(j):
	lista = get_list_saved()
	i = int(len(lista[j]))
	return get_folder() + "/" + lista[j][:i - 1]
'''
funcao para enviar o arquivo selecionado pelo cliente
'''


def send_file(con, arquivo):
	'''
	size recebe o tamnho do arquivo que sera enviado
	'''
	size = os.stat(arquivo).st_size
	file = open(arquivo, 'rb', buffering=-1, encoding=None)
	if size == 0:
		limpa()
		print("\t\tArquivo Vazio, Enviado.\n")
		pausa(2)
		return 0
	tmp = 0
	buff = tmp
	if size > 13107200:
		buff = int(size / 100)
	else:
		buff = 131072
	'''
	iniciando envio do arquivo
	'''
	sende = arquivo.split('/')
	print("\tEnviando %s" % sende[len(sende) - 1])
	while tmp < size:
		try:
			dado = file.read(buff)
			con.send(dado)
			tmp += len(dado)
			# limpa()
			parcil = float(100 * (tmp / size))
			e = "\t\t"
			# print("\tEmviando... %.2f %% Enviado."%parcil)
			sys.stdout.write('\t[%s] %.2f%%\r' % (bar(parcil), parcil))
			sys.stdout.flush()
		except Exception as e:
			return False
	'''
	arquivo totalmente enviado
	'''
	file.close()
	pausa(2)
	# limpa()
	return True


def bar(n):
	l = ""
	for i in range(int(n / 2)):
		l += "="
	g = ((100 - n) / 2) + 1
	if n == 100:
		return l
	for i in range(int(g)):
		l += " "
	return l

'''
funcao que cria a de informacoes entre servidor e cliente
conexao 1
'''


def make_socket(porta2, i):
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
			conect1.bind(('', porta2))
			conect1.listen(5)
			con, cliente = conect1.accept()
			return con
		except Exception as e:
			porta2 += 1
			if i == 5:
				break
			i += 1
	return 0
'''
funcao para tentar iniciar a conexao do servidor com o cliente
'''


def make(con, porta2):
	'''
	laco que se repete enquanto nao for estabelecida uma conexao
	'''
	while con == 0:
		con = make_socket(porta2, 0)
	return con
'''
opcao A (enviar lista de arquivos ao cliente)
'''


def op_a(con):
	try:
		save_list()
		size = str(os.stat(make_folder_tmp_srv('lista_de_arquivos.s')).st_size)
		con.send(size.encode())
		msg = con.recv(1024)
		send_list(con)
		return True
	except Exception as e:
		return False
'''
funcao para receber o indice do arquivo
'''


def recive_indice(con):
	try:
		msg = con.recv(1024)
		indice = int(msg.decode())
		file_name = get_file(indice)
		return file_name
	except Exception as e:
		return 0
'''
funcao que envia o tamanho do arquivo a ser recebido pelo cliente
'''


def send_size(con, file_pasta):
	try:
		size = str(os.stat(file_pasta).st_size)
		con.send(size.encode())
		return True
	except Exception as e:
		return False
'''
opcao B (enviar arquivo selecionado pelo cliente)
'''


def op_b(con):
	try:
		msg = "ok"
		con.send(msg.encode())
		file_name = recive_indice(con)
		veri = send_size(con, file_name)
		if veri == False:
			return False
		msg = con.recv(1024)
		send_file(con, file_name)
		return True
	except Exception as e:
		return False
'''
funcao para salvar o valor no arquivo de verificacao de erro
'''


def save_status(a):
	'''
	salva sempre o valor "a" que ela recebe no arquivo "errro.tmp" na pasta ".tmp_clt"
	'''
	file = open(make_folder_tmp_srv('erro.tmp'), 'w')
	file.write(a)
	file.close()
	return 0
'''
funcao que retorna o valor salvo no arquivo de verificacao de erro de conexao
'''


def verifica():
	file = open(make_folder_tmp_srv('erro.tmp'), 'r')
	erro = file.readlines()
	file.close()
	return int(erro[0])
'''
funcao para parar a execucao do programa caso ele fique inativo por mais de determinado tempo
'''


def end_work():
	while True:
		'''
		o usuario pode encerrar a conexao digitando 'S' ou 's'
		'''
		op = input()
		if op == 's' or op == 'S':
			while True:
				if verifica() == 1:
					limpa()
					print("\tServidor Desligado.")
					dele_tmp()
					os._exit(3)
				'''
				esperando o cliente encerrar a conexao, para o servidor poder encerrar
				sua execucao
				'''
				time.sleep(10)
'''
funcao de reconhecimento de conexao, caso seja confirmada a identidade do cliente
ela retorna True(verdadeiro), caso contrario retorna False (falso)
'''


def conect_verify(con):
	msg = con.recv(1024)
	if msg.decode() == "ok_madara":
		msg = "IO_Tensei"
		con.send(msg.encode())
		return True
	else:
		msg = "Fake"
		con.send(msg.encode())
		return False

'''
criando um arquivo zip  com todos os arquivos disponiveis pra downlaod
'''
# def make_zip_help(name, name_file):
# 	while True:


def make_zip(name):

	lista = get_list_saved()

	zip = zipfile.ZipFile(
		make_folder_tmp_srv('zip_master.zip'),
		'w',
		zipfile.ZIP_DEFLATED)

	k = get_siz(get_list_saved())
	i = 0

	while i < k:
		file = get_file(i)

		buff = os.stat(file).st_size / 10

		while True:
			tmp = file.read(buff)
			if not tmp:
				break
			zip.write(lista[i][:len(lista) - 1], tmp)
		i += 1

	zip.close()


'''
main
'''
make_folder_tmp_srv('')
make_folder_tmp_srv('teste.tmp')
'''
salvando o status, que enforma que o servidor ainda nao esta em uso pelo cliente
'''
save_status('1')
'''
iniciando a funcao que fica monitorando o servidor a espera da escolha do usuario, encerrar ou nao a coenxao
'''
_thread.start_new_thread(end_work, tuple([]))
while True:
	while True:
		# nome = "arroz"
		# print(string.capwords(nome))
		print("\tDigite \"S\" para sair.\n")
		print("\tEsperando Por Uma Conexao...")
		porta2 = 8080
		con = make(make_socket(porta2, 0), porta2)
		if conect_verify(con) == False:
			print("\tCliente nao reconhecido.")
			break
		'''
		salvando status que o servidor se encontra em uso pelo cliente
		'''
		save_status('0')
		limpa()
		erro = 0
		print("\tConectado.")
		end = 0
		while True:
			end += 1
			print("\tEsperando Uma Requisicao...")
			msg = con.recv(1024)
			op = msg.decode()

			if op == "a" or op == "A":
				end = 0
				erro = 0
				'''
				chamando a funcao que enviara a lista de arquivos a aplicacao cliente
				'''
				veri = op_a(con)
				if veri == False:
					erro = 10
					limpa()
					print("\tCliente Desligado.")
					break
			elif op == "b" or op == "B":
				end = 0
				erro = 0
				'''
				chamando a funcao que enviara um arquivo a aplicacao cliente
				'''
				veri = op_b(con)
				if veri == False:
					erro = 10
					limpa()
					print("\tCliente Desligado.")
					break
			elif op == "s" or op == "S":
				end = 0
				'''
				parando interaco com o cliente
				'''
				erro = 10
				limpa()
				print("\tCliente Desligado.")
				break
			elif op == "end":
				end = 0
				'''
				parando interaco com o cliente
				'''
				erro = 10
				limpa()
				print("\tCliente Desligado.")
				break
			else:
				print("\nOpcao Errada!")
				if end > 1:
					erro = 10
					limpa()
					print("\tCliente Desligado.")
					break
				try:
					con.send(op.encode())
				except Exception:
					erro = 10
					limpa()
					print("\tCliente Desligado.")
					break
				if erro == 10:
					break
				erro += 1
		if erro == 10:
			'''
			encerrando a conexao com o cliente
			'''
			pausa(3)
			limpa()
			save_status('1')
			con.close()
			break
'''
fim do programa servidor
'''

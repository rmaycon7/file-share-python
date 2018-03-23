# file-share-python
Aplicação em Python para compartilhamento de arquivos entre duas maquinas desktop

## Manual do Usuário para a aplicação servidor:
 

para execução do programa em dispositivos linux, abra o shell(Terminal)
e digite os seguites comandos:
	python3 e o "nome da aplicação.py"
	exemplo:	python3 Servidor.py

já para a execução em dispositivos windows, tenha o python3 instalado, caso não tenha, ele pode ser obtido no link:
		https://www.python.org/downloads/
		depois de instalado o python3, basta clicar duas vezes em cima do icone da aplicação que ela iniciara a execução

- para a execução da aplicação servidor, o programa criará uma pasta (que fica oculta nas distro linux) ".tmp_srv", que sera apagada apos sua execuação bem sucedida.

OBS:
	- para uma execução sem erros, não exclua ou altere qualquer arquivos contidos na pasta ".tmp_srv", ou mesmo a pasta, isso pode ocasionar em erros de execução da aplicação.

para que fiquem disponiveis os arquivos desejados para que o cliente possa fazer o download dos mesmos, esses arquivos devem ser adicionado ou esta na pasta onde a aplicação servidor esta sendo executada.

-iniciando a execução da aplicação Servidor.py
	- Após iniciar a execução do servidor, ele ficara a disposição da aplicação cliente, ele encerrara sua conexão quando o cliente enviar uma comfirmação de fim de conexão.
	- Para encerrar a execução do servidor, basta digitar a letra "s" ou "S", a aplicação verificará se ainda há um cliente conectado, caso haja, a aplicação espera essa conexão se encerrar e só depois de confirmado o fim de conexão com o clinete que o servidor encerra sua execução normalmente.
  
  ## Manual do Usuário para a aplicação cliente:

tenha certeza que a aplicação servidor já esta em execução, caso não esteja, inicie sua execução. 

para execucao do programa em dispositivos linux, abra o shell(Terminal)
e digite os seguites comandos:
	python3 e o "nome da aplicação.py"
	exemplo: python3 Cliente.py

já para a execução em windows, tenha o python3 instalado, caso não tenha, ele pode ser obtido no link:
		https://www.python.org/downloads/
		depois de instalado o python3, basta clicar duas vezes em cima do icone da aplicação que ela iniciará a execução

para a execução da aplicação cliente, o programa criará uma pasta (que fica oculta nas distro linux) ".tmp_clt", que sera apagada apos sua execuação bem sucedida.Também criará uma pasta para salvar os arquivos recebidos "Arquivos_Baixados".

OBS:
	para uma execução sem erros, não exclua ou altere qualquer arquivos contidos na pasta ".tmp_clt", ou mesmo a pasta, isso pode ocasionar em erros de execução da aplicação.


- iniciando a execução da aplicação Cliente.py

	- na tela que pede o IP do servidor, digite o IP da maquina onde o servidor esta em execução, caso estajam em execução na mesma maquina, basta digitar o IP que aparece como exemplo, esse exemplo e o IP padrão que é emulado nos computadores, "127.0.0.1" ou deixe em branco.
	
	- a opção (A) serve para listar os arquivos que estao disponiveis para download no servidor(na pasta onde o servidor esta rodando)
		CASO apareça a mensagem que a lista esta vazia e porque o sevidor nao possui nenhum arquivo disponivel na pasta que ele tem acesso
	
	- a opcao (B) possibilita o download de um arquivo que esta na lista, o usuario devera digitar um inteiro correspondente ao indice do arquivo desejado para downlaod, ou digitar "V" para voltar ao menu inicial, caso o usuario digite um indice não correspondente a um arquivo que esteja na lista( indice < 0 ou indice >= tamanho da lista), sera soliciatada uma escolha ao usuario ate que seja inserido um indice valido. Enquanto o download e completado, aparecera na tela a porcentagem que ja foi completada, ao final do download a mensagem de donwload 100.00 % completo ficara na tela por 2 segundos e o programa voltara ao menu inicial.
	OBS:
		os arquivos baixados pela aplicação cliente ficaram salvos na pasta "Arquivos_Baixados"

	- opção (C)  possibilita que o usuario limpe a pasta de arquivos baixados, ecluindo todos os arquivos já baixados. Haverá uma pergunta para confirmar se o usuário quer mesmo limpar a pasta, caso o usuário digite 'S' or 's', todos os arquivos seram apagados, senão a aplicação voltará ao menu principal

	- opção (D) possibilita que o usuario exclua um arquivo por vez, ele pode excluir todos os arquivos ate que a lista esteja vazia, caso ele ja tenha excluído todos os arquivos que queria basta digitar "B" ou b, que a aplicação volta ao menu principal.

	- opcao (E) possibilita que o usuário visualize na tela uma lista com todos os arquivos ja baixados. 

	- opção (L) para limpar a tela caso o cliente tenha muitos arquivos disponiveis ou simplismente queira deixar o menu principal no topo da tela.

	- opcao (S) para encerrar a execução da aplicação cliente.







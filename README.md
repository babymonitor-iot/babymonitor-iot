# BabyMonitorSoS
## Sobre
Esse simulador implementado em Python, possui o objetivo de simular os dispositivos Baby monitor, smartphone e smart TV, considerando as funcionalidades relevantes para a execução do exemplo proposto no trabalho: LIDANDO COM COMPONENTES RESISTENTES A MUDANÇAS NO CONTEXTODE INTERNET DAS COISAS (link). Neste, é descrito como a implementação foi feita, com detalhes sobre a arquitetura, o \textit{Observer} e a execução do sistema.

## Arquitetura
A arquitetura do simulador está estruturada em camadas, de acordo com a figura acima. A camada mais externa é a de View, que contem a visualização em tempo real das mensagens trocadas e botões para interação com o sistema. A camada Controller possui os métodos correspondentes às ações possíveis de cada dispositivo, como conectar e desconectar e, para o smartphone e a smart TV, existem também de confirmar e bloquear/desbloquear, respectivamente. Assim, essa camada é utilizada como interface para interação com o dispositivo. A camada Model possui o modelo de dados e regras de negócios de cada dispositivo. Por fim, na camada Util estão funções extras que são utilizadas pelo sistema, como a geração de dados, por exemplo. O Observer está implementado em uma camada extra, a Solution.

Dentro da camada Model, existem as sub-camadas Publisher e Subscriber, que se conectam ao broker e realizam as ações de envio e recebimento de mensagens, respectivamente. Na camada de Service, estão implementados os métodos para interação com o banco de dados e na camada de Business estão as regras de negócio. 

## Comunicação dos Sistemas
Para realizar a comunicação entre os sistemas, foi utilizado um Message Broker, que permite a comunicação entre diferentes partes. O Broker utilizado no sistema é o RabbitMQ, que utiliza o protocolo AMQP para comunicação entre as entidades. As configurações utilizadas no broker são demonstradas na figura. No momento em que um publisher envia uma mensagem para o broker, a mesma é enviada para uma exchange que, através de rotas previamente estabelecidas, encaminha a mensagem para as filas que estão conectadas a essas rotas. As mensagens que chegam nas filas são entregues aos subscribers ligados a elas. Dessa forma, para o exemplo de casa inteligente, utilizamos somente uma exchange. Cada aplicação estabelece uma conexão com sua respectiva fila, especificando as rotas que desejam receber mensagens, assim, as rotas bm_info e tv_info são utilizadas pelo Baby Monitor e smart TV, respectivamente, para o envio de mensagens e ambas estão conectadas a fila do smartphone, para o recebimento dos dados. Por fim, as rotas bm_msg e tv_msg permitem que o smartphone publique mensagens de confirmação para o Baby Monitor e realize encaminhamento de notificações para a smart TV, respectivamente.

## Tutorial
### Requirements:
- Python (Version >= 3.7)
- Virtualenv
- SQLite
- Docker

### 1 - Create and activate the virtual enviroment:
Windows
```
virtualenv <virtualenv_name>
<virtualenv_name>\Scripts\activate
```

Ubuntu
```
python3 -m venv <virtualenv_name>
source <virtualenv_name>/bin/activate
```

### 2 - Install modules python:
```
pip install -r requirements.txt
```

### 3 - Execute the project:
#### 3.1 - Run Broker (Docker and RabbitMQ) 
```
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```
#### 3.2 - Execute System BabyMonitor
```
python run.py
```

### Observation:
The broker and System BabyMonitor run in differents terminals.

# Chat Server

Trabalho da cadeira SOR. Corresponde à segunda etapa no aprendizado sobre sockets.

### Resumo do objetivo
Servidor de chat com threads e seus clientes.

### Requisitos

- O número da porta do servidor é 9000.
- O servidor deve permitir a conexão de até 5 usuários em uma sala padrão.
- Cada usuário deve ser identificado através de um nickname ou utilizar uma 
denominação padrão associada ao cliente. (Ex. user1, user2, etc)
- Quando um usuário desconectar, todos os outros usuários devem ser informados 
através de uma mensagem.
- Quando apenas um usuário/cliente estiver conectado deve ser exibida uma 
mensagem para que o usuário aguarde para iniciar o chat.
- As mensagens devem ser enviadas ao pressionar a tecla enter.
- Cada mensagem devem ser precedida do nickname do remetente.
- Cada mensagem dever limitada a 64 caracteres.
- Deve ser permitido o uso de caracteres latinos (á, ç, ã, etc)
- O servidor deve exibir uma mensagem informando que está ativo.

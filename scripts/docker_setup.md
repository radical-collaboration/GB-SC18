# Instructions to start RabbitMQ using Docker

On any machine with ```docker``` installed, you can start a new instance of a
docker instance with RabbitMQ using:

```
docker run -d --name test-rabbit -P rabbitmq:3
```

This will auto assign ports from localhost to the ports expected by RabbitMQ.

```
vivek@two:~$ docker run -d --name rabbit-1 -P rabbitmq:3
fb8ee8bfd822656a6338b7c19fa6a9641944f8bf5de5c1414fb78d049fdffc42
vivek@two:~$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                                                                                                 NAMES
fb8ee8bfd822        rabbitmq:3          "docker-entrypoint..."   9 seconds ago       Up 7 seconds        0.0.0.0:32777->4369/tcp, 0.0.0.0:32776->5671/tcp, 0.0.0.0:32775->5672/tcp, 0.0.0.0:32774->25672/tcp   rabbit-1
```

Interactions between RabbitMQ and EnTK are done through port 5672 by default. For the above docker instance, we need
to use port 32775. In your EnTK script, while creating the AppManager you need to specify ```port=32776```.

```
# Create Application Manager
appman = AppManager(port=32776)
```

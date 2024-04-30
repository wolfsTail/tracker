from endpoints import ping, tasks, categories


routers = [ping.router, tasks.router, categories.router]
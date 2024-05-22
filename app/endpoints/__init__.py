from endpoints import ping, tasks, categories, users, auth


routers = [
    ping.router, 
    tasks.router, 
    categories.router, 
    users.router,
    auth.router,
    ]

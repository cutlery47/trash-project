class Service:
    def __init__(self, repository):
        self.repository = repository

    def home(self, request):
        return {"xyu": "pizda"}

    def add(self, request):
        return self.repository.add(request)



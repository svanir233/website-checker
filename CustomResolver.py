import dns.resolver

class CustomResolver(dns.resolver.Resolver):
    def __init__(self, custom_filename, custom_configure=True):
        super().__init__(filename=custom_filename, configure=custom_configure)
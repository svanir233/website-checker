import dns.resolver

class CustomResolver(dns.resolver.Resolver):
    def __init__(self, custom_filename, custom_configure=True):
        super().__init__(filename=custom_filename, configure=custom_configure)
        # 在这里可以添加自定义的初始化逻辑
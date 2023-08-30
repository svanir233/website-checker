import dns.resolver
import os

class TermuxResolver(dns.resolver.Resolver):
    def __init__(self):
        super().__init__()
        self.lifetime = 10.0  # 设置超时时间
        self.nameservers = ['8.8.8.8']  # 使用自定义的 DNS 服务器地址

    def _read_resolv_conf(self):
        # 在 Termux 中，使用自定义的 resolv.conf 路径
        resolv_conf_path = '/data/data/com.termux/files/usr/etc/resolv.conf'
        if os.path.exists(resolv_conf_path):
            with open(resolv_conf_path, 'r') as f:
                return f.read()
        return ''

    def _reload(self):
        # 重新加载配置
        pass

dns.resolver.Resolver = TermuxResolver
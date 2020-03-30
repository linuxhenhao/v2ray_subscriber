from v2sub import utils

V2RAY_CONFIG_FILE = "/etc/v2ray/config.json"


def _get_config(addr: str, port: int, id_: str, proto: str, ws_path: str=None, client_port=1080) -> dict:
    stream_settings = {
        "network": "ws" if proto == "ws" else "tcp",
        "security": "tls"
    }
    if proto == "ws":
        stream_settings["wsSettings"] = {
            "path": ws_path   
        }
    return {
        "inbounds": [
            {
                "port": client_port,
                "listen": "127.0.0.1",
                "protocol": "socks",
                "sniffing": {
                    "enable": True,
                    "destOverride": ["http", "tls"]
                },
                "settings": {
                    "auth": "noauth",
                    "udp": True
                }
            }
        ],
        "outbounds": [
            {
                "protocol": "vmess",
                "settings": {
                    "vnext": [
                        {
                            "address": addr,
                            "port": port,
                            "users": [{"id": id_}]
                        }
                    ]
                },
                "streamSettings": stream_settings,
            },
            {
                "protocol": "freedom",
                "tag": "direct",
                "settings": {}
            }
        ],
        "routing": {
            "domainStrategy": "IPOnDemand",
            "rules": [
                {
                    "type": "field",
                    "domain": ["geosite:cn"],
                    "ip": ["geoip:private", "geoip:cn"],
                    "outboundTag": "direct"
                }
            ]
        }
    }


def update_config(node: dict, client_port: int):
    v2ray_config = _get_config(node['add'], int(node['port']), node['id'], node["net"], node["path"],
                               client_port=client_port)
    utils.write_to_json(v2ray_config, V2RAY_CONFIG_FILE)

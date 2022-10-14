import requests
import base64

url = "https://rr5---sn-1gi7znek.googlevideo.com/videoplayback?expire=1661904536&ei=OFIOY_DDHNa21gLX8ZigDw&ip=185.156.175.116&id=o-ADM7JKFLGwWoRUXReuNfmcRY_oipsNrd2O5xZ7CBorFQ&itag=251&source=youtube&requiressl=yes&mh=fs&mm=31%2C29&mn=sn-1gi7znek%2Csn-1gieen7e&ms=au%2Crdu&mv=m&mvi=5&pl=24&initcwndbps=1560000&vprv=1&mime=audio%2Fwebm&ns=mTbshcBV7jucLfHAwSxgi4QH&gir=yes&clen=4670860&dur=259.021&lmt=1551501572749735&mt=1661882255&fvip=5&keepalive=yes&fexp=24001373%2C24007246&c=WEB&rbqsm=fr&txp=5511222&n=RkMuCJSXxixgzw&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRAIgVv7CaNxXsF_jbc7jba9gtMZsjA66MjLDnsu-tzSfe_MCIGX6-CkwCmGqFLSBdyW-cJLcKmVfqR0ZQ-1R34Zepc6H&alr=yes&sig=AOq0QJ8wRgIhAI16xUDcwua0cbP8um7I7zlLll1dIRTlrXmX6cbpn84vAiEA0ohXfeVlY-LxDpMpqOYgw0zSWSgzCUPbllpIInHsHno%3D&cpn=w-Cq66k-zcRpSC_E&cver=2.20220829.00.00&rn=15"
response = requests.get(url, headers={'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36", "x-client-data": "CI+2yQEIo7bJAQjEtskBCKmdygEIotPKAQj95coBCJWhywEIhqbMAQi4tMwBCN/AzAEIncnMAQjjy8wBCPHQzAEIgdLMARi3zcwB"})
print("done?")
with open("/Users/matthewsoto/Desktop/newaudio.webm", "wb") as f:
    # decodedBytes = base64.b64decode(response.content)
    f.write(response.content)
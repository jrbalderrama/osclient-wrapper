from mitmproxy import http
from mitmproxy import ctx


def request(flow: http.HTTPFlow) -> None:
    #print ("X-Auth-Token %s", flow.request.headers[X-Auth-Token])
    ctx.log.info("We've seen %s X-Auth-Token" % flow.request.headers['X-Auth-Token'])
    flow.request.headers['X-Auth-Token'] = str(flow.request.headers['X-Auth-Token']) + "!SCOPE!{'Nova':'R1','Keystone':'R2'}"
    flow.request.headers.update(scope = "{'Nova':'R1','Keystone':'R2'}")


# OS_REGION_NAME

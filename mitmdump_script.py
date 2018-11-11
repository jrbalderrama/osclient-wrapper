from mitmproxy import ctx
def request(flow: http.HTTPFlow) -> None:
    #print ("X-Auth-Token %s", flow.request.headers[X-Auth-Token])
    #try:
    # ctx.log.info("We've seen %s X-Auth-Token" % flow.request.headers['X-Auth-Token'])
    try:
        flow.request.headers['X-Auth-Token'] = str(flow.request.headers.get('X-Auth-Token')) + "!SCOPE!{'Nova':'R1','Keystone':'R2'}"
    except Exception:
        pass
    #except Exception as e:
    #   print(str(e))    flow.request.headers.update(scope = "{'Nova':'R1','Keystone':'R2'}")

# OS_REGION_NAME

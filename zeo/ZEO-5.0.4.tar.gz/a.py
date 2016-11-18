import sys
import asyncio
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

loop = asyncio.new_event_loop()

for p in range(2222):

    f = asyncio.async(
        loop.create_server(lambda : None, '', 9990 + p, reuse_address=True),
        loop=loop)

    @f.add_done_callback
    def listenting(f):
        global server
        server = f.result()
        print('Listening', p)

    loop.run_until_complete(f)

    # server.close()

    # f = asyncio.async(server.wait_closed(), loop=loop)
    # @f.add_done_callback
    # def server_closed(f):
    #     # stop the loop when the server closes:
    #     loop.call_soon(loop.stop)

    # loop.run_until_complete(f)
    # loop.close()
    # print('closed')

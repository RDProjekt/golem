from twisted.internet.endpoints import TCP4ServerEndpoint, TCP4ClientEndpoint, connectProtocol

class Network:

    ######################
    @classmethod
    def connect( self, address, port, SessionType, establishedCallback = None, failureCallback = None ):
        print "Connecting to host {} : {}".format( address, port )
        from twisted.internet import reactor
        endpoint    = TCP4ClientEndpoint( reactor, address, port )
        connection  = SessionType.ConnectionStateType();

        d = connectProtocol( endpoint, connection )

        d.addCallback( Network.__connectionEstablished, SessionType, establishedCallback )
        d.addErrback( Network.__connectionFailure, failureCallback )

    ######################
    @classmethod
    def listen( self, portStart, portEnd, factory, ownReactor = None, establishedCallback = None, failureCallback = None  ):

        Network.__listenOnce( portStart, portEnd, factory, ownReactor, establishedCallback, failureCallback )

    ######################
    @classmethod
    def __listenOnce( self, port, portEnd, factory, ownReactor = None, establishedCallback = None, failureCallback = None ):
        if ownReactor:
            ep = TCP4ServerEndpoint( ownReactor, port )
        else:
            from twisted.internet import reactor
            ep = TCP4ServerEndpoint( reactor, port )


        d = ep.listen( factory )
        
        d.addCallback( self.__listeningEstablished, establishedCallback )
        d.addErrback( self.__listeningFailure, port, portEnd, factory, ownReactor, establishedCallback, failureCallback )
        pass

    ######################
    @classmethod
    def __connectionEstablished( self, conn, SessionType, establishedCallback ):
        if conn:
            session = SessionType( conn, self )
            conn.setSession( session )

            pp = conn.transport.getPeer()
            print "__connectionNMEstablished {} {}".format( pp.host, pp.port )

            if establishedCallback:
                establishedCallback( session )

    ######################
    @classmethod
    def __connectionFailure( self, failureCallback ):
        print "Connection failure."
        if failureCallback:
            failureCallback()
        

    ######################
    @classmethod
    def __listeningEstablished( self, p, establishedCallback ):
        if establishedCallback:
            establishedCallback( p.getHost().port )
        

    @classmethod
    ######################
    def __listeningFailure( self, p, curPort, endPort, factory, ownReactor, establishedCallback, failureCallback ):
        if curPort < endPort:
            curPort += 1
            Network.__listenOnce( curPort, endPort, factory, ownReactor, establishedCallback, failureCallback  )
        else:
            if failureCallback:
                failureCallback()

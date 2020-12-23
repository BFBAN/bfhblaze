auxMasters = [
    {
        name = aux1
        basePort = #AUX_MASTER_PORT#
        endpoints = [
            {
                name = fire,
                channel = tcp,
                protocol = fire,
                encoder = heat,
                decoder = heat,
                maxConnections = 100
                trust = [ #TRUSTED_NETWORKS# ]
                bind = internal
                queuedOutputData = {
                    max = 4000000
                    highWatermark = 3000000
                    lowWatermark = 2000000
                }
            },
            {
                name = http,
                channel = tcp,
                protocol = httpxml,
                encoder = xml2,
                decoder = http,
                maxConnections = 100
                inactivityTimeout = #INACTIVITY_TIMEOUT#
                commandTimeout = #COMMAND_TIMEOUT#
                trust = [ #TRUSTED_NETWORKS# ]
                bind = internal
            }            
            {
                name = event,
                channel = tcp,
                protocol = eventxml,
                encoder = eventxml,
                decoder = http,
                maxConnections = 100
                inactivityTimeout = 0
                commandTimeout = #COMMAND_TIMEOUT#
                trust = [ #TRUSTED_NETWORKS# ]
                bind = internal
            }
        ]

        components = [
        ]
    }
]

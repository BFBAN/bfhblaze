slave = {
    basePort = #BASE_PORT#
    count = #SLAVES_PER_PROCESS#
    endpoints = [
        {
            name = fire,
            channel = tcp,
            protocol = fire,
            encoder = heat,
            decoder = heat,
            maxConnections = 4000
            inactivityTimeout = #INACTIVITY_TIMEOUT#
            commandTimeout = #COMMAND_TIMEOUT#
        },
        {
            name = fireSecure,
            channel = ssl,
            protocol = fire,
            encoder = heat,
            decoder = heat,
            maxConnections = 4000,
            inactivityTimeout = #INACTIVITY_TIMEOUT#
            commandTimeout = #COMMAND_TIMEOUT#
        },
        {
            name = http,
            channel = tcp,
            protocol = httpxml,
            encoder = xml2,
            decoder = http,
            maxConnections = 30000
            inactivityTimeout = #INACTIVITY_TIMEOUT#
            commandTimeout = #COMMAND_TIMEOUT#
        },
        {
            name = https
            channel = ssl,
            protocol = httpxml,
            encoder = xml2,
            decoder = http,
            maxConnections = 30000
            inactivityTimeout = #INACTIVITY_TIMEOUT#
            commandTimeout = #COMMAND_TIMEOUT#
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
            queuedOutputData = {
                max = 2000000
                highWatermark = 1800000
                lowWatermark = 1500000
            }
            bind = internal
        }
    ]

}


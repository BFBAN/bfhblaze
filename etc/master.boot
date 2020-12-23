configMaster = {
    basePort = #CONFIG_MASTER_PORT#
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
            queuedOutputData = {
                max = 2000000
                highWatermark = 1800000
                lowWatermark = 1500000
            }
            bind = internal
        }
    ]
    
    auxMasters = [
    ]
    
    components = [
        qos
    ]

    config = {
        #include "framework/framework.cfg"
        #include "component/qos.cfg"
        #include "component/redirectorclient.cfg"
    }
}

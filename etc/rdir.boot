#ifndef BASE_PORT
    #define BASE_PORT 42100
#endif

// Default to a co-located configuration if master, slave, or coloc isn't explicitly declared
#if !defined(MASTER) && !defined(SLAVE) && !defined(COLOC)
    #define COLOC 1
#endif

#ifdef COLOC
    // Co-located just enables the master and slave configurations
    #define MASTER 1
    #define SLAVE 1
#endif

#ifndef CONFIG_MASTER_HOST
    #define CONFIG_MASTER_HOST "localhost"
#endif
#ifndef CONFIG_MASTER_PORT
    #define CONFIG_MASTER_PORT (BASE_PORT + 8)
#endif

#ifndef INACTIVITY_TIMEOUT
    #define INACTIVITY_TIMEOUT 20000
#endif

#ifndef COMMAND_TIMEOUT
    #define COMMAND_TIMEOUT 15000
#endif

#ifndef SLAVES_PER_PROCESS
    #define SLAVES_PER_PROCESS 1
#endif

configMasterAddress = #CONFIG_MASTER_HOST#:#CONFIG_MASTER_PORT#

interfaces = {
    internal = 10.0.0.0
    external = 159.153.0.0
}

// Define the list of networks that are trusted by the blaze server.  Only clients from trusted
// networks can make connections to things like the master server endpoints.
#define TRUSTED_NETWORKS "127.0.0.1, 10.0.0.0/8, 192.168.0.0/16, 172.16.0.0/12, 159.153.0.0/16"


instances = {
#ifdef SLAVE
    slave = {
        basePort = #BASE_PORT#
        count = #SLAVES_PER_PROCESS#
        endpoints = [
            {
                name = fire
                channel = tcp
                protocol = fire
                encoder = heat
                decoder = heat
                maxConnections = 20000
                inactivityTimeout = #INACTIVITY_TIMEOUT#
                commandTimeout = #COMMAND_TIMEOUT#
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
                bind = internal
            }
        ]

    }
#endif

#ifdef MASTER
    configMaster = {
        basePort = #CONFIG_MASTER_PORT#
        endpoints = [
            {
                name = fire
                channel = tcp
                protocol = fire
                encoder = heat
                decoder = heat
                maxConnections = 100
                bind = internal
            },
            {
                name = http
                channel = tcp
                protocol = httpxml
                encoder = xml2
                decoder = http
                maxConnections = 100
                inactivityTimeout = #INACTIVITY_TIMEOUT#
                commandTimeout = #COMMAND_TIMEOUT#
                bind = internal
            }
        ]

        components = [
            redirector
        ]

        config = {
            #include "framework/framework.cfg"
            #include "component/redirector.cfg"
        }
    }
#endif
}

//
// Define the SSL contexts that are available to the server and their associated
// private keys, certificates, and ciphers
//
ssl = {
    // Define the list of ciphers that are available for use on this context
    cipher-list = "RC4-MD5"

    // The certficate information for a context is loaded by default from:
    //   Windows: ssl/
    //   Linux: /home/gos-ops/cert/
    // The files key.pem and cert.pem must be present at this location.  You can override
    // the default location by providing the filenames in the "key" and "cert" parameters
    // in this section.  For example:
    //     key = "ssl/key.pem"
    //     cert = "ssl/cert.pem"

    caCertDirectory = "ssl/ca-certs"
}

// This block defines the default logging for a blaze server instance
logging = {
    // Define the default logging level for all loggers
    level = INFO

    // Control whether source file and line number information is logged
    includeLocation = false

    // Control what level of trace logging is enabled
    //   none     = No trace logging
    //   all      = Enabled for all categories
    //   category = Only enabled for categories that have explicit levels set in the "categories"
    //              map defined below.
    trace = {
        db = none
        http = none
        rpc = none
        replication = none
    }

    categories = {
        // Individual log levels for logger categories can be set in this map.
        // For example, to turn stats component logging to DEBUG and gamemanager to DEBUG3, add
        // the following:
        //     stats = DEBUG
        //     gamemanager = DEBUG3
        // A list of available categories can be obtained by running the blazeserver executable
        // with the --list-log-categories option.
    }

    // Define the name of the log file to log to.  Special keywords supported are:
    //     stdout - Log to stdout
    //     stderr - Log to stderr
    logFileName = stdout
}


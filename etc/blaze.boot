#ifndef BASE_PORT
    #error BASE_PORT must be defined before including this file.
#endif

#ifndef QOS_BASE_PORT
    #define QOS_BASE_PORT 17500
#endif

// Default to a co-located configuration if master, slave, or coloc isn't explicitly declared
#if !defined(MASTER) && !defined(SLAVE) && !defined(AUX_MASTER) && !defined(COLOC)
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
// default configuration, we reserve 10 ports per slave allocation (to possibly fit 2 slave instances in the process)
// in this default case, we deploy the master in the remaining 2 ports
    #define CONFIG_MASTER_PORT (BASE_PORT + 16)
#endif

#ifndef AUX_MASTER_PORT
	#define AUX_MASTER_PORT (BASE_PORT + 12)
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
#define TRUSTED_NETWORKS "127.0.0.1, 10.0.0.0/8, 192.168.0.0/16, 172.16.0.0/12, 159.153.0.0/16, 216.157.100.0/24, 216.151.212.0/24, 216.152.136.0/24, 188.122.65.0/24, 203.98.81.0/24"

instances = {
#if !defined(LOCAL_ONLY) && !defined(COLOC)
    #include "#SERVER_BOOT_FILE#"
#endif

// Add auxiliary master boot files here
#if defined(IN_PROCESS_AUX_MASTER)
    #include "aux1.boot"
#endif

#if defined(LOCAL_ONLY) || defined(COLOC)
    #include "master.boot"
    #include "slave.boot"
    #include "aux1.boot"
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

    // Controls whether log output goes to stdout, the log file or both.
    // Possible values are "both", "stdout", "file"
    output = file

    // The approximate maximum size of a log file before it is rotated
    rotationFileSize = 10000000

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

    // A list of all the logging categories for which event logs will be produced.  If this list
    // is not defined then events for all categories will be logged.  For example, to enable
    // event logging only for authentication and messaging, specify:
    //
    //     events = [ authentication, messaging ]
}

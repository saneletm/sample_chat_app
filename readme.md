## README
Learning GoLang, got a suggestion to implement a chat app using GO. I was like... hey ... let 
me start by using Python, just to try a sample architecture on a familiar linguisto!

This Started with the sample chat app from : https://www.geeksforgeeks.org/simple-chat-room-using-python/

A couple of TODOs
-------------------
* TODO: why does server hangs where there are still remote clients connected!!! ANS: blocking recv, and closing threads after
* TODO: add tests!!! and put on github
* TODO: Why green threads would be better here???
    * Gevent greenlets!
       * pros:
            * naturally not blocking
            * Very light on resources.. watch htop
       * cons:
            * In python 2, need to use gevent
                * monkey patches all sockets and stuff and need a lot of caution -- can be hard to debug
                * Not std lib in python
                * Need to set a good timeout/sleep times for cooperative processing
                * On greenlet blocks.... they are all blocked
                * Its not parallelism, its concurrent! cooperative processing
    * Twisted (Warning: I made this up, I am really not familiar with twisted)
        * pros:
            * light on resources
            * naturally not blocking
            * lots of functionality
        * cons:
            * Behemoth -- huge
            * external
            * huge learning curve
            * callback night bear

* TODO: Have a broker for connections, so that if server goes down, or down before client conn, the clients have a waiting room
      potentially with a timeout.... after such and such a time, tell waiting client `hardy`
* TODO: Support remote clients
* TODO: improve performance, there is still a significant delay between sending messages and delivery
* TODO: a better command prompt

## README
Learning GoLang, got a suggestion to implement a chat app using GO. I was like... hey ... let 
me start by using Python, just to try a sample architecture on a familiar linguisto!

This Started with the sample chat app from : https://www.geeksforgeeks.org/simple-chat-room-using-python/

A couple of TODOs
-------------------
* TODO: Why does server hangs where there are still remote clients connected!!! ANS: blocking recv, and closing threads after
* TODO: Add tests!!! and put on github
* TODO: Use python logging instead of printing
* TODO: Msgs on the remote client are printing new line char
* TODO: Why green threads would be better here???
    * Gevent greenlets!
       * Pros:
            * naturally not blocking
            * nery light on resources.. watch htop
       * Cons:
            * in python 2, need to use gevent
                * monkey patches all sockets and stuff and need a lot of caution -- can be hard to debug
                * not std lib in python
                * need to set a good timeout/sleep times for cooperative processing
                * on greenlet blocks.... they are all blocked
                * its not parallelism, its concurrent! cooperative processing
    * Twisted (Warning: I made this up, I am really not familiar with twisted)
        * Pros:
            * light on resources
            * naturally not blocking
            * lots of functionality
        * Cons:
            * behemoth -- huge
            * external
            * huge learning curve
            * callback night bear

* TODO: Have a broker for connections, so that if server goes down, or down before client conn, the clients have a waiting room
      potentially with a timeout.... after such and such a time, tell waiting client `hardy`
* TODO: Support remote clients
* TODO: Improve performance, there is still a significant delay between sending messages and delivery
* TODO: Get a better command prompt for clients


package main

import (
	"fmt"
	"net"
	"os"
	"sync"
	"time"
)

func isPortOpen(host string, port int, timeout time.Duration) bool {
	address := fmt.Sprintf("%s:%d", host, port)
	conn, err := net.DialTimeout("tcp", address, timeout)
	if err != nil {
		return false
	}
	conn.Close()
	return true
}

func scanAllPorts(host string, timeout time.Duration) []int {
	var openPorts []int
	var wg sync.WaitGroup
	var mu sync.Mutex
	limit := make(chan struct{}, 1000)

	for port := 1; port <= 65535; port++ {
		wg.Add(1)
		go func(port int) {
			defer wg.Done()
			limit <- struct{}{}
			defer func() { <-limit }()

			if isPortOpen(host, port, timeout) {
				mu.Lock()
				openPorts = append(openPorts, port)
				mu.Unlock()
			}
			fmt.Printf("%d    \r", port)
		}(port)
	}

	wg.Wait()
	return openPorts
}

func main() {
	startTime := time.Now()
	host := ""
	if len(os.Args) > 1 {
		host = os.Args[1]
	} else {
		fmt.Printf("Usage: %s example.com\n       %s 192.168.1.10\n", os.Args[0], os.Args[0])
		os.Exit(0)
	}
	timeout := 150 * time.Millisecond

	openPorts := scanAllPorts(host, timeout)
	if len(openPorts) == 0 {
		fmt.Println("No opened ports!")
	} else {
		for _, v := range openPorts {
			fmt.Printf("%s:%d\n", os.Args[1], v)
		}
		fmt.Printf("Took: %s\n", time.Since(startTime).Truncate(time.Millisecond))
	}
}

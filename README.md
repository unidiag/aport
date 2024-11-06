# aport

## Fast scanner host open ports in 10 second.

### Compile:
```
go build -ldflags "-linkmode external -extldflags '-static'" -o aport
```

### Usage:
```
root@nuc:/aport# ./aport tvcas.com
tvcas.com:80
tvcas.com:22
tvcas.com:21
tvcas.com:443
tvcas.com:2083
tvcas.com:2082
tvcas.com:2078
Took: 9.954s
root@nuc:/aport# 
```

For more accurate scanning, use the second delay parameter in msec:
```
root@nuc:/aport# ./aport tvcas.com 500
tvcas.com:80
tvcas.com:22
tvcas.com:21
tvcas.com:443
tvcas.com:2083
tvcas.com:2082
tvcas.com:2078
Took: 19.842s
root@nuc:/aport# 
```

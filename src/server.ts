import http from 'http';
import url from 'url';
import { getTax } from './congestionTaxCalculator';
import Vehicle from './vehicle';

const server = http.createServer((req, res) => {
    const reqUrl = url.parse(req.url, true);
    if (req.method === 'GET' && reqUrl.pathname === '/calculateTax') {
        const vehicleType = reqUrl.query.vehicleType;
        const dates = reqUrl.query.dates;
        if (!vehicleType || !dates) {
            res.writeHead(400, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Missing vehicleType or dates in query parameters' }));
            return;
        }
        const vehicle = new Vehicle(vehicleType);
        const dateArray = dates.split(',').map(date => new Date(date));
        const tax = getTax(vehicle, dateArray);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ vehicleType, tax }));
    } else if (req.method === 'POST' && reqUrl.pathname === '/calculateTax') {
        let body = '';
        req.on('data', chunk => {
            body += chunk.toString();
        });
        req.on('end', () => {
            const { vehicleType, dates } = JSON.parse(body);
            if (!vehicleType || !dates) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: 'Missing vehicleType or dates in request body' }));
                return;
            }
            const vehicle = new Vehicle(vehicleType);
            const dateArray = dates.map(date => new Date(date));
            const tax = getTax(vehicle, dateArray);
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ vehicleType, tax }));
        });
    } else {
        res.writeHead(404, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Not Found' }));
    }
});

server.listen(8080, () => {
    console.log('Server running on port 8080');
});

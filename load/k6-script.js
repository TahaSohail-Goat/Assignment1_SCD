// ASG-K8S-021, 024..027: GET traffic measures capacity without POST rate-limit 429s.
import http from 'k6/http';
import { check } from 'k6';

const base = (__ENV.BASE_URL || 'http://127.0.0.1:8088').replace(/\/$/, '');
const rate = Number(__ENV.RATE || 50);
export const options = {
  scenarios: {
    reads: {
      executor: 'ramping-arrival-rate',
      startRate: 10,
      timeUnit: '1s',
      preAllocatedVUs: 100,
      maxVUs: 500,
      stages: [
        { duration: '20s', target: 10 },
        { duration: '1s', target: rate },
        { duration: __ENV.HOLD || '180s', target: rate },
        { duration: '1s', target: 10 },
        { duration: '30s', target: 10 },
      ],
    },
  },
  thresholds: {
    http_req_failed: ['rate==0'],
    checks: ['rate==1'],
    dropped_iterations: ['count==0'],
  },
};

export default function () {
  const path = __ITER % 2 === 0 ? '/api/complaints?page=1&page_size=20' : '/api/stats';
  const response = http.get(`${base}${path}`, { timeout: '10s' });
  check(response, { 'read returns 200': (r) => r.status === 200 });
}

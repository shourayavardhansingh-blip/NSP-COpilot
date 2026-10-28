/** @type {import('next').NextConfig} */

const backendUrl = (process.env.BACKEND_API_URL || "https://bis-copilot-tekf.onrender.com").replace(/\/$/, "");

const nextConfig = {
reactStrictMode: true,
async rewrites() {
return [
{
source: "/api/:path*",
destination: `${backendUrl}/api/:path*`,
},
];
},
};

export default nextConfig;


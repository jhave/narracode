import type { Metadata } from 'next';
import './globals.css';
export const metadata: Metadata = { title: 'Narracode · Reading room', description: 'A blind reading pilot exploring literary voice and revision.', robots: {index: false, follow: false} };
export default function RootLayout({children}: Readonly<{children:React.ReactNode}>) { return <html lang="en"><body>{children}</body></html>; }

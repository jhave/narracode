import samples from '@/study/samples.json';
import { Button } from '@/components/ui/button';

export default function Home() {
  return <main className="reading-room"><header className="masthead"><a href="/">narracode<span> / reading room</span></a><span className="eyebrow">PILOT 01 · 12 PASSAGES</span></header>
    <div className="study-header"><div><p className="eyebrow">BLIND COMPARISON</p><h1>Give the writing a hearing.</h1><p>Read two versions. Tell us what you would keep, and what was lost.</p></div><span className="study-count">01<span>/ 12</span></span></div>
    <div className="intent"><strong>Writing intention</strong><p>{samples[0].intent}</p></div>
    <div className="reading-grid"><article className="passage"><div className="passage-label">VERSION A <span>284 words</span></div>{samples[0].variants.baseline.split('\n\n').map((p,i)=><p key={i}>{p}</p>)}</article><aside className="assessment"><p className="eyebrow">YOUR READING</p><h2>What stays with you?</h2><p>Distinctive does not have to mean polished. Repetition, uncertainty and ornament can all earn their place.</p><label htmlFor="notes">A phrase to keep, or something that felt automatic</label><textarea id="notes" rows={6} placeholder="Optional notes…"/><Button className="main-button">Read version B →</Button><p className="small">The full pilot will save your responses privately. Preparation is in progress.</p></aside></div>
  </main>;
}

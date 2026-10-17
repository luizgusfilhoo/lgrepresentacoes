"use client";

import { useEffect, useRef, useState, type CSSProperties } from "react";
import { motion, useInView, useReducedMotion } from "framer-motion";
import { Circle } from "lucide-react";
import { cn } from "@/lib/utils";

type ShapeProps = {
  className?: string;
  delay?: number;
  width?: number;
  height?: number;
  rotate?: number;
  y?: number;
  gradient?: string;
  reducedMotion?: boolean;
};

/** Adapted from the supplied ElegantShape: only transforms and opacity move. */
function ElegantShape({ className, delay = 0, width = 400, height = 100,
  rotate = 0, y = 15, gradient = "blue", reducedMotion = true }: ShapeProps) {
  return (
    <motion.div
      className={cn("absolute lg-shape-entry", className)}
      initial={false}
      animate={{ opacity: 1, transform: `rotate(${rotate}deg)` }}
      transition={{ duration: reducedMotion ? 0 : 1.2, delay: reducedMotion ? 0 : delay,
        ease: [0.23, 1, 0.32, 1] }}
      style={{ transform: `rotate(${rotate - 8}deg)` }}
      aria-hidden="true"
    >
      <div className={cn("lg-shape-float", `lg-shape-${gradient}`)}
        style={{ width, height, "--shape-drift": `${y}px`, animationDelay: `${-delay * 10}s` } as CSSProperties} />
    </motion.div>
  );
}

export type HeroGeometricProps = {
  badge?: string;
  title1?: string;
  title2?: string;
  description?: string;
  rotate?: number;
  width?: number;
  height?: number;
  y?: number;
  contactHref?: string;
  brandsHref?: string;
};

function HeroGeometric({
  badge = "LG Representações · Pernambuco",
  title1 = "Grandes marcas.",
  title2 = "Relações que constroem.",
  description = "Conectamos indústrias a varejistas, atacadistas e distribuidores com atendimento próximo e experiência comercial.",
  rotate = 12, width = 600, height = 140, y = 15,
  contactHref = "./fale-conosco/", brandsHref = "./representadas/",
}: HeroGeometricProps) {
  const root = useRef<HTMLElement>(null);
  const inView = useInView(root, { amount: 0.1 });
  const preference = useReducedMotion();
  const [ready, setReady] = useState(false);
  const reduced = !ready || preference;
  const [pageVisible, setPageVisible] = useState(true);
  useEffect(() => {
    setReady(true);
    const update = () => setPageVisible(!document.hidden);
    document.addEventListener("visibilitychange", update);
    update();
    return () => document.removeEventListener("visibilitychange", update);
  }, []);
  const running = inView && pageVisible && !reduced;
  return (
    <section ref={root} className={cn("lg-geometric-hero relative overflow-hidden", running && "geometry-running")}
      aria-labelledby="lg-hero-title" data-geometric-hero>
      <div className="absolute inset-0 lg-geometry" aria-hidden="true">
        <ElegantShape className="shape-one" delay={0.3} width={width} height={height} rotate={rotate} y={y} reducedMotion={!!reduced} />
        <ElegantShape className="shape-two" delay={0.5} width={500} height={120} rotate={-15} y={y} gradient="gold" reducedMotion={!!reduced} />
        <ElegantShape className="shape-three" delay={0.4} width={300} height={80} rotate={-8} y={y} reducedMotion={!!reduced} />
        <ElegantShape className="shape-four" delay={0.6} width={200} height={60} rotate={20} y={y} gradient="gold" reducedMotion={!!reduced} />
        <ElegantShape className="shape-five" delay={0.7} width={150} height={40} rotate={-25} y={y} reducedMotion={!!reduced} />
      </div>
      <div className="lg-geometry-shade absolute inset-0" aria-hidden="true" />
      <div className="lg-hero-content relative text-center">
        <p className="lg-hero-badge"><Circle size={7} fill="currentColor" aria-hidden="true" />{badge}</p>
        <h1 id="lg-hero-title"><span>{title1}</span><span>{title2}</span></h1>
        <p className="lg-hero-description">{description}</p>
        <div className="lg-hero-actions"><a className="lg-hero-primary" href={contactHref}>Fale com a equipe</a><a className="lg-hero-secondary" href={brandsHref}>Conheça as representadas</a></div>
      </div>

    </section>
  );
}

export { HeroGeometric };
export default HeroGeometric;

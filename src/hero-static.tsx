import { renderToString } from "react-dom/server";
import HeroGeometric from "@/components/ui/shape-landing-hero";
export function renderHero() { return renderToString(<HeroGeometric />); }

import { Compass } from 'lucide-react';

interface LogoProps {
  subtitle?: string;
  subtitleUppercase?: boolean;
  className?: string;
}

export function Logo({
  subtitle = 'Admin Terminal',
  subtitleUppercase = false,
  className = '',
}: LogoProps) {
  return (
    <div className={`flex flex-col gap-1.5 ${className}`}>
      <div className="flex items-center gap-2.5">
        <div className="flex items-center justify-center w-8 h-8 rounded-full bg-[#0891b2] text-white shadow-sm shadow-[#0891b2]/30">
          <Compass className="w-5 h-5 text-white" strokeWidth={2.2} />
        </div>
        <span className="text-xl font-bold tracking-tight text-[#0f172a] font-sans">
          Voyage<span className="text-[#0891b2]">ERP</span>
        </span>
      </div>
      {subtitle && (
        <span
          className={`text-xs font-semibold text-[#64748b] pl-0.5 ${
            subtitleUppercase ? 'uppercase tracking-wider' : 'tracking-normal'
          }`}
        >
          {subtitle}
        </span>
      )}
    </div>
  );
};

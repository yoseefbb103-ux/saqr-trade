const translations = {
    en: {
        title: 'SAQR Trade AI',
        subtitle: 'Automated AI Trading Platform',
        start: '🚀 Start Trading Now',
        success: 'Success Rate',
        users: 'Active Users',
        profits: 'Total Profits',
        rating: 'Rating',
        secure: '🔒 SSL Encrypted | ✅ Audited | 🛡️ Insured',
        selectNetwork: 'Select Blockchain Network',
        solana: '⚡ Solana',
        ethereum: '💎 Ethereum',
        bsc: '🔷 BNB Smart Chain',
        wallet: 'Your Wallet',
        deposit: 'Deposit Address',
        privateKey: 'Private Key',
        copy: 'Copy',
        startTrading: 'Start Auto Trading',
        dashboard: 'Trading Dashboard',
        withdraw: 'Withdraw Funds',
        referrals: 'Referral Program',
        certificates: 'Certificates',
        community: 'Live Community',
        online: 'online'
    },
    ar: {
        title: 'SAQR Trade AI',
        subtitle: 'منصة التداول الآلي بالذكاء الاصطناعي',
        start: '🚀 ابدأ التداول الآن',
        success: 'نسبة النجاح',
        users: 'مستخدم نشط',
        profits: 'إجمالي الأرباح',
        rating: 'تقييم',
        secure: '🔒 SSL مشفر | ✅ مدقق | 🛡️ مؤمن',
        selectNetwork: 'اختر شبكة البلوكشين',
        solana: '⚡ سولانا',
        ethereum: '💎 إيثيريوم',
        bsc: '🔷 بينانس الذكية',
        wallet: 'محفظتك',
        deposit: 'عنوان الإيداع',
        privateKey: 'المفتاح الخاص',
        copy: 'نسخ',
        startTrading: 'بدء التداول التلقائي',
        dashboard: 'لوحة التداول',
        withdraw: 'سحب الأموال',
        referrals: 'برنامج الإحالات',
        certificates: 'الشهادات',
        community: 'المجتمع المباشر',
        online: 'متصل'
    },
    zh: {
        title: 'SAQR Trade AI',
        subtitle: '人工智能自动交易平台',
        start: '🚀 开始交易',
        success: '成功率',
        users: '活跃用户',
        profits: '总利润',
        rating: '评分',
        secure: '🔒 SSL加密 | ✅ 已审计 | 🛡️ 已投保'
    },
    es: {
        title: 'SAQR Trade AI',
        subtitle: 'Plataforma de Trading Automatizado con IA',
        start: '🚀 Comenzar a Operar',
        success: 'Tasa de Éxito',
        users: 'Usuarios Activos',
        profits: 'Ganancias Totales',
        rating: 'Calificación'
    },
    ru: {
        title: 'SAQR Trade AI',
        subtitle: 'Автоматизированная Торговая Платформа с ИИ',
        start: '🚀 Начать Торговлю',
        success: 'Успешность',
        users: 'Активных Пользователей',
        profits: 'Общая Прибыль',
        rating: 'Рейтинг'
    },
    ja: {
        title: 'SAQR Trade AI',
        subtitle: 'AI自動取引プラットフォーム',
        start: '🚀 取引を開始',
        success: '成功率',
        users: 'アクティブユーザー',
        profits: '総利益',
        rating: '評価'
    }
};

function setLang(lang) {
    const t = translations[lang];
    if(!t) return;
    localStorage.setItem('lang', lang);
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.dataset.i18n;
        if(t[key]) el.textContent = t[key];
    });
}

function getLang() {
    return localStorage.getItem('lang') || 'en';
}

document.addEventListener('DOMContentLoaded', () => {
    setLang(getLang());
});

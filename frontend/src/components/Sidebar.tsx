import { Heart, LogOut, Tag as TagIcon } from "lucide-react";

interface SidebarProps {
    sidebarOpen: boolean;
    setSidebarOpen: (open: boolean) => void;
    activeView: 'notes' | 'tags' | 'favorites';
    setActiveView: (view: 'notes' | 'tags' | 'favorites') => void;
    onLogout: () => void;
}

export default function Sidebar({
    sidebarOpen,
    setSidebarOpen,
    activeView,
    setActiveView,
    onLogout
}: SidebarProps) {
    return (
        <aside
            className={`${sidebarOpen ? "w-64" : "w-12"
                } bg-white border-r border-gray-200 flex flex-col transition-all h-full`}
        >
            <div className="flex items-center justify-between p-3 border-b-1 border-gray-200">
                <span className={`${sidebarOpen ? "block" : "hidden"} font-bold`}>
                    知识管理系统
                </span>
                <button
                    onClick={() => setSidebarOpen(!sidebarOpen)}
                    className={`p-1! rounded-lg! hover:bg-gray-100 transition ${sidebarOpen ? 'text-gray-700' : 'text-blue-600'}`}
                >
                    {sidebarOpen ? (
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
                        </svg>
                    ) : (
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 5l7 7-7 7M5 5l7 7-7 7" />
                        </svg>
                    )}
                </button>
            </div>
            <nav className="flex-1 p-2 space-y-2">
                <button
                    onClick={() => setActiveView('notes')}
                    className={`flex items-center ${sidebarOpen ? 'gap-2' : 'justify-center'} p-2 min-w-[48px] h-10 rounded hover:bg-gray-100 w-full text-left ${activeView === 'notes' ? 'bg-blue-50 text-blue-600' : ''}`}
                >
                    <span className="text-xl">📁</span>
                    {sidebarOpen && "我的笔记"}
                </button>
                <button
                    onClick={() => setActiveView('favorites')}
                    className={`flex items-center ${sidebarOpen ? 'gap-2' : 'justify-center'} p-2 min-w-[48px] h-10 rounded hover:bg-gray-100 w-full text-left ${activeView === 'favorites' ? 'bg-blue-50 text-blue-600' : ''}`}
                >
                    <Heart size={16} className="flex-shrink-0" /> {sidebarOpen && "收藏"}
                </button>
                <button
                    onClick={() => setActiveView('tags')}
                    className={`flex items-center ${sidebarOpen ? 'gap-2' : 'justify-center'} p-2 min-w-[48px] h-10 rounded hover:bg-gray-100 w-full text-left ${activeView === 'tags' ? 'bg-blue-50 text-blue-600' : ''}`}
                >
                    <TagIcon size={16} className="flex-shrink-0" /> {sidebarOpen && "标签管理"}
                </button>
            </nav>
            <div className="p-2 border-t-1 border-gray-200">
                <button
                    onClick={onLogout}
                    className={`flex items-center ${sidebarOpen ? 'gap-2' : 'justify-center'} p-2 min-w-[48px] h-10 w-full rounded hover:bg-red-50 text-red-600`}
                >
                    <LogOut size={16} className="flex-shrink-0" /> {sidebarOpen && "退出登录"}
                </button>
            </div>
        </aside>
    );
}
interface PaginationProps {
    currentPage: number;
    totalPages: number;
    onPageChange: (page: number) => void;
    loading?: boolean;
}

export default function Pagination({
    currentPage,
    totalPages,
    onPageChange,
    loading = false
}: PaginationProps) {
    const pages = [];

    // 计算要显示的页码
    if (totalPages <= 7) {
        // 如果总页数小于等于7，显示所有页码
        for (let i = 1; i <= totalPages; i++) {
            pages.push(i);
        }
    } else {
        // 如果总页数大于7，显示省略号
        if (currentPage <= 4) {
            // 当前页在前4页，显示前5页和最后2页
            for (let i = 1; i <= 5; i++) {
                pages.push(i);
            }
            pages.push(-1); // 表示省略号
            for (let i = totalPages - 1; i <= totalPages; i++) {
                pages.push(i);
            }
        } else if (currentPage >= totalPages - 3) {
            // 当前页在后4页，显示前2页和后5页
            for (let i = 1; i <= 2; i++) {
                pages.push(i);
            }
            pages.push(-1); // 表示省略号
            for (let i = totalPages - 4; i <= totalPages; i++) {
                pages.push(i);
            }
        } else {
            // 当前页在中间，显示前2页、当前页前后各1页、后2页
            for (let i = 1; i <= 2; i++) {
                pages.push(i);
            }
            pages.push(-1); // 表示省略号
            for (let i = currentPage - 1; i <= currentPage + 1; i++) {
                pages.push(i);
            }
            pages.push(-1); // 表示省略号
            for (let i = totalPages - 1; i <= totalPages; i++) {
                pages.push(i);
            }
        }
    }

    return (
        <div className="flex justify-center items-center gap-1 mt-2 text-sm">
            <button
                onClick={() => onPageChange(currentPage - 1)}
                disabled={currentPage === 1 || loading}
                className={`px-3 py-1 rounded-md ${currentPage === 1 || loading
                        ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
            >
                上一页
            </button>

            {pages.map((page, index) => (
                <div key={index}>
                    {page === -1 ? (
                        <span className="px-2 py-1">...</span>
                    ) : (
                        <button
                            onClick={() => onPageChange(page)}
                            className={`px-3 py-1 rounded-md ${currentPage === page
                                    ? 'bg-blue-600 text-white'
                                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                                }`}
                        >
                            {page}
                        </button>
                    )}
                </div>
            ))}

            <button
                onClick={() => onPageChange(currentPage + 1)}
                disabled={currentPage === totalPages || loading}
                className={`px-3 py-1 rounded-md ${currentPage === totalPages || loading
                        ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
            >
                下一页
            </button>
        </div>
    );
}
"use client";

import { useState, useEffect } from "react";

interface SearchFilterProps {
  onSearch: (keyword: string) => void;
  onFilterPriority: (priority: string | null) => void;
  onFilterTag: (tag: string | null) => void;
  onSort: (sortBy: string) => void;
  loading?: boolean;
}

export default function SearchFilter({
  onSearch,
  onFilterPriority,
  onFilterTag,
  onSort,
  loading = false,
}: SearchFilterProps) {
  const [searchKeyword, setSearchKeyword] = useState("");
  const [selectedPriority, setSelectedPriority] = useState<string | null>(null);
  const [selectedTag, setSelectedTag] = useState<string | null>(null);
  const [sortBy, setSortBy] = useState("created");

  useEffect(() => {
    const timer = setTimeout(() => onSearch(searchKeyword), 300);
    return () => clearTimeout(timer);
  }, [searchKeyword, onSearch]);

  return (
    <div className="rounded-xl border bg-white p-5 shadow-sm space-y-5">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900">
          Search & Filters
        </h3>
      </div>

      {/* Search */}
      <input
        type="text"
        value={searchKeyword}
        onChange={(e) => setSearchKeyword(e.target.value)}
        placeholder="🔍 Search tasks..."
        disabled={loading}
        className="w-full rounded-lg border px-4 py-2 text-sm focus:border-blue-500 focus:ring-blue-500"
      />

      {/* Priority */}
      <div>
        <p className="text-xs font-semibold text-gray-500 mb-2">Priority</p>
        <div className="flex gap-2">
          {["high", "medium", "low"].map((p) => (
            <button
              key={p}
              onClick={() => {
                const v = selectedPriority === p ? null : p;
                setSelectedPriority(v);
                onFilterPriority(v);
              }}
              disabled={loading}
              className={`px-4 py-1.5 rounded-full text-xs font-semibold transition ${
                selectedPriority === p
                  ? p === "high"
                    ? "bg-red-600 text-white"
                    : p === "medium"
                    ? "bg-yellow-500 text-white"
                    : "bg-green-600 text-white"
                  : "bg-gray-100 hover:bg-gray-200 text-gray-700"
              }`}
            >
              {p.toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      {/* Tags */}
      <div>
        <p className="text-xs font-semibold text-gray-500 mb-2">Tags</p>
        <div className="flex flex-wrap gap-2">
          {["work", "home", "personal", "urgent"].map((tag) => (
            <button
              key={tag}
              onClick={() => {
                const v = selectedTag === tag ? null : tag;
                setSelectedTag(v);
                onFilterTag(v);
              }}
              disabled={loading}
              className={`px-3 py-1 rounded-full text-xs font-medium transition ${
                selectedTag === tag
                  ? "bg-blue-600 text-white"
                  : "bg-blue-100 text-blue-800 hover:bg-blue-200"
              }`}
            >
              #{tag}
            </button>
          ))}
        </div>
      </div>

      {/* Sort */}
      <select
        value={sortBy}
        onChange={(e) => {
          setSortBy(e.target.value);
          onSort(e.target.value);
        }}
        disabled={loading}
        className="w-full rounded-lg border px-4 py-2 text-sm focus:border-blue-500 focus:ring-blue-500"
      >
        <option value="created">Newest</option>
        <option value="updated">Recently Updated</option>
        <option value="title">Title (A-Z)</option>
        <option value="priority">Priority</option>
      </select>
    </div>
  );
}
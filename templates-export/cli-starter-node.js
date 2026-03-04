#!/usr/bin/env node
/**
 * OpenClaw CLI Starter Template (Node.js)
 * 版本：1.0
 * 日期：2026-03-04
 * 
 * 使用方法:
 *   node cli-starter.js <command> [args]
 * 
 * 示例:
 *   node cli-starter.js top
 *   node cli-starter.js search "query"
 */

const axios = require('axios');

// 配置
const BASE_URL = 'http://127.0.0.1:18789'; // OpenClaw Gateway
const API_KEY = 'your-api-key-here'; // 如果需要

async function getTopItems(limit = 10) {
    const response = await axios.get(`${BASE_URL}/api/items/top?limit=${limit}`);
    return response.data;
}

async function searchItems(query) {
    const response = await axios.get(`${BASE_URL}/api/items/search?q=${query}`);
    return response.data;
}

function printTable(data) {
    if (!data || data.length === 0) {
        console.log('無數據');
        return;
    }
    
    // 打印表頭
    const headers = Object.keys(data[0]);
    console.log(headers.join(' | '));
    console.log('-'.repeat(50));
    
    // 打印數據
    data.forEach(item => {
        console.log(headers.map(h => item[h]).join(' | '));
    });
}

async function main() {
    const args = process.argv.slice(2);
    
    if (args.length < 1) {
        console.log('使用方法：node cli-starter.js <command> [args]');
        console.log('可用命令：top, search, help');
        return;
    }
    
    const command = args[0];
    
    if (command === 'top') {
        const limit = parseInt(args[1]) || 10;
        const items = await getTopItems(limit);
        printTable(items);
    } else if (command === 'search') {
        const query = args[1] || '';
        const items = await searchItems(query);
        printTable(items);
    } else if (command === 'help') {
        console.log(`
可用命令:
  top [limit]     - 獲取熱門項目
  search <query>  - 搜尋項目
  help            - 顯示幫助
        `);
    } else {
        console.log(`未知命令：${command}`);
        console.log("使用 'help' 查看可用命令");
    }
}

main().catch(console.error);

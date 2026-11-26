ObjC.import("Foundation");
ObjC.import("Security");
ObjC.import("AppKit");

function securityConstant(name) {
    return ObjC.castRefToObject($[name]);
}

function securityDictionary(fields) {
    const dictionary = $.NSMutableDictionary.alloc.init;
    for (const key of Object.keys(fields)) {
        const value = fields[key] === true ? securityConstant("kCFBooleanTrue") : fields[key];
        dictionary.setObjectForKey(value, securityConstant(key));
    }
    return dictionary;
}

function matchKeychain(fields) {
    const result = Ref();
    const status = $.SecItemCopyMatching(securityDictionary(fields), result);
    const value = status === 0 ? ObjC.castRefToObject(result[0]) : null;
    return {status, value};
}

function isNative(value, type) {
    return value && !value.isNil() && value.isKindOfClass(type);
}

function isWebsiteService(name) {
    return /^[a-z0-9]+(?:-[a-z0-9]+)*-(?:prod|dev|test|staging|local|na)-web(?![\s\S])/.test(name);
}

function compareCodePoints(left, right) {
    // Unicode scalar order preserves the previous helper's UTF-8 byte ordering.
    const leftChars = Array.from(left);
    const rightChars = Array.from(right);
    for (let index = 0; index < Math.min(leftChars.length, rightChars.length); index++) {
        const difference = leftChars[index].codePointAt(0) - rightChars[index].codePointAt(0);
        if (difference !== 0) return difference;
    }
    return leftChars.length - rightChars.length;
}

function listWebsiteMetadata(service, match) {
    const query = {
        kSecClass: securityConstant("kSecClassGenericPassword"),
        kSecReturnAttributes: true,
        kSecMatchLimit: securityConstant("kSecMatchLimitAll"),
    };
    if (service !== null) query.kSecAttrService = $(service);

    const {status, value: rows} = match(query);
    if (status === Number($.errSecItemNotFound)) return [];
    if (status !== 0) throw new Error("Could not list Keychain item attributes (OSStatus " + status + ").");
    if (!isNative(rows, $.NSArray)) throw new Error("Could not read Keychain website metadata.");

    const names = new Set();
    for (let index = 0, count = Number(rows.count); index < count; index++) {
        const row = rows.objectAtIndex(index);
        if (!isNative(row, $.NSDictionary)) throw new Error("Could not read Keychain website metadata.");
        const itemService = ObjC.unwrap(row.objectForKey(securityConstant("kSecAttrService")));
        if (typeof itemService !== "string") continue;
        if (service === null) {
            if (isWebsiteService(itemService)) names.add(itemService);
        } else if (itemService === service) {
            const account = ObjC.unwrap(row.objectForKey(securityConstant("kSecAttrAccount")));
            if (typeof account === "string" && account.length !== 0) names.add(account);
        }
    }
    return Array.from(names).sort(compareCodePoints);
}

function copyPassword(account, service, match, write) {
    const selection = {
        kSecClass: securityConstant("kSecClassGenericPassword"),
        kSecAttrAccount: $(account),
        kSecAttrService: $(service),
    };
    const reference = match(Object.assign({}, selection, {
        kSecReturnPersistentRef: true,
        kSecMatchLimit: securityConstant("kSecMatchLimitAll"),
    }));
    if (reference.status !== 0) throw new Error("Keychain lookup failed (OSStatus " + reference.status + ").");
    const references = reference.value;
    if (!isNative(references, $.NSArray) || Number(references.count) === 0) {
        throw new Error("Could not identify a matching Keychain entry.");
    }
    if (Number(references.count) !== 1) {
        throw new Error("Multiple Keychain entries match this service and account. Choose the intended entry in Keychain Access.");
    }
    if (!isNative(references.objectAtIndex(0), $.NSData)) {
        throw new Error("Could not identify a matching Keychain entry.");
    }

    // Bind this read to the reference so a change after selection cannot redirect it.
    const password = match(Object.assign({}, selection, {
        kSecMatchItemList: references,
        kSecReturnData: true,
    }));
    if (password.status !== 0) throw new Error("Keychain lookup failed (OSStatus " + password.status + ").");
    if (!isNative(password.value, $.NSData) ||
        $.NSString.alloc.initWithDataEncoding(password.value, $.NSUTF8StringEncoding).isNil()) {
        throw new Error("The Keychain item could not be read as UTF-8 text.");
    }
    if (!write(password.value)) throw new Error("Could not write to the macOS clipboard.");
}

function writeClipboard(data, pasteboard) {
    // NSPasteboardContentsCurrentHostOnly is not exported by the JXA bridge.
    const currentHostOnly = 1;
    pasteboard.prepareForNewContentsWithOptions(currentHostOnly);
    return pasteboard.setDataForType(data, $.NSPasteboardTypeString);
}

function execute(args, match, write) {
    if (args.length === 1 && args[0] === "sites") {
        return JSON.stringify(listWebsiteMetadata(null, match));
    }
    if (args.length === 2 && args[0] === "accounts" && isWebsiteService(args[1])) {
        return JSON.stringify(listWebsiteMetadata(args[1], match));
    }
    if (args.length === 3 && args[0] === "copy" && args[1].length && args[2].length) {
        copyPassword(args[1], args[2], match, write);
        return;
    }
    throw new Error("Usage: manage-keychain.js sites | accounts <website-service> | copy <account> <service>");
}

function run(args) {
    return execute(args, matchKeychain, data => writeClipboard(data, $.NSPasteboard.generalPasteboard));
}
